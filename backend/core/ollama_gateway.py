import json
from collections.abc import Callable
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from backend.core.model_gateway import ModelGateway, ModelRequest, ModelResponse

_MAX_RESPONSE_BYTES = 1_048_576
_MAX_REQUEST_BYTES = 256_000
_MAX_MODEL_OUTPUT = 20_000
_ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1"}
_OLLAMA_PORT = 11434


class _NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(req.full_url, code, "redirects are disabled", headers, fp)


class OllamaModelGateway(ModelGateway):
    """Local-only Ollama gateway with a fixed loopback endpoint."""

    def __init__(
        self,
        *,
        model: str,
        base_url: str = "http://127.0.0.1:11434",
        timeout_seconds: float = 30.0,
        opener: Callable[..., object] | None = None,
    ) -> None:
        model = model.strip()
        if not model or len(model) > 128:
            raise ValueError("model must be 1-128 characters")

        parsed = urlparse(base_url)
        if parsed.scheme != "http" or parsed.hostname not in _ALLOWED_HOSTS:
            raise ValueError("Ollama gateway accepts only HTTP loopback endpoints")
        if parsed.port not in (None, _OLLAMA_PORT):
            raise ValueError("Ollama gateway accepts only the default Ollama port")
        if parsed.path not in ("", "/"):
            raise ValueError("Ollama gateway accepts only the base loopback path")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Ollama endpoint must not contain credentials or query data")
        if timeout_seconds <= 0 or timeout_seconds > 120:
            raise ValueError("timeout must be between 0 and 120 seconds")

        self._url = f"http://{parsed.hostname}:{_OLLAMA_PORT}/api/chat"
        self._model = model
        self._timeout = timeout_seconds
        self._opener = opener or build_opener(_NoRedirectHandler())

    def generate(self, request: ModelRequest) -> ModelResponse:
        request.validate_bounds()
        if request.temperature != 0:
            raise ValueError("Ollama gateway currently requires temperature=0")

        payload = {
            "model": self._model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
            "stream": False,
            "options": {"temperature": 0},
        }
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        if len(body) > _MAX_REQUEST_BYTES:
            raise ValueError("model request body exceeds 256KB")

        http_request = Request(
            self._url,
            data=body,
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            opener = self._opener
            if hasattr(opener, "open"):
                with opener.open(http_request, timeout=self._timeout) as response:
                    raw = response.read(_MAX_RESPONSE_BYTES + 1)
            else:
                with opener(http_request, timeout=self._timeout) as response:
                    raw = response.read(_MAX_RESPONSE_BYTES + 1)
        except Exception as exc:
            raise RuntimeError("local Ollama request failed") from exc

        if len(raw) > _MAX_RESPONSE_BYTES:
            raise RuntimeError("Ollama response exceeds the configured size limit")
        try:
            document = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError("Ollama returned an invalid JSON response") from exc

        message = document.get("message")
        output = message.get("content") if isinstance(message, dict) else None
        if not isinstance(output, str) or not output.strip():
            raise RuntimeError("Ollama response did not contain bounded text output")

        return ModelResponse(
            provider="ollama",
            model=self._model,
            content=output[:_MAX_MODEL_OUTPUT],
            finish_reason="stop" if document.get("done") else None,
        )
