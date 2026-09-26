import json
from collections.abc import Callable
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from backend.core.model_gateway import ModelGateway, ModelRequest, ModelResponse

_MAX_RESPONSE_BYTES = 1_048_576
_ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1"}


class OllamaModelGateway(ModelGateway):
    """Local-only Ollama gateway; it cannot be pointed at arbitrary hosts."""

    def __init__(
        self,
        *,
        model: str,
        base_url: str = "http://127.0.0.1:11434",
        timeout_seconds: float = 30.0,
        opener: Callable[..., object] = urlopen,
    ) -> None:
        if not model.strip() or len(model) > 128:
            raise ValueError("model must be 1-128 characters")
        parsed = urlparse(base_url)
        if parsed.scheme != "http" or parsed.hostname not in _ALLOWED_HOSTS:
            raise ValueError("Ollama gateway accepts only HTTP loopback endpoints")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Ollama endpoint must not contain credentials or query data")
        if timeout_seconds <= 0 or timeout_seconds > 120:
            raise ValueError("timeout must be between 0 and 120 seconds")
        self._url = base_url.rstrip("/") + "/api/chat"
        self._model = model.strip()
        self._timeout = timeout_seconds
        self._opener = opener

    def generate(self, request: ModelRequest) -> ModelResponse:
        request.validate_bounds()
        if request.temperature != 0:
            raise ValueError("Ollama gateway currently requires temperature=0")
        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": False,
            "options": {"temperature": 0},
        }
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        if len(body) > 256_000:
            raise ValueError("model request body exceeds 256KB")
        http_request = Request(
            self._url,
            data=body,
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            with self._opener(http_request, timeout=self._timeout) as response:
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
            content=output[:20_000],
            finish_reason="stop" if document.get("done") else None,
        )
