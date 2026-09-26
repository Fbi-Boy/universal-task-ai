import json
from collections.abc import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from backend.core.model_gateway import ModelGateway, ModelRequest, ModelResponse
from backend.core.secret_provider import SecretProvider

_OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
_MAX_RESPONSE_BYTES = 1_048_576

class OpenAIModelGateway(ModelGateway):
    """Bounded server-side OpenAI Responses API gateway."""
    def __init__(self, secret_provider: SecretProvider, *, model: str,
                 timeout_seconds: float = 30.0,
                 opener: Callable[..., object] = urlopen) -> None:
        if not model.strip() or len(model) > 128:
            raise ValueError("model must be 1-128 characters")
        if timeout_seconds <= 0 or timeout_seconds > 120:
            raise ValueError("timeout must be between 0 and 120 seconds")
        self._secrets = secret_provider
        self._model = model.strip()
        self._timeout = timeout_seconds
        self._opener = opener

    def generate(self, request: ModelRequest) -> ModelResponse:
        request.validate_bounds()
        if request.temperature != 0:
            raise ValueError("OpenAI Responses gateway currently requires temperature=0")
        api_key = self._secrets.get("openai_api_key", env_name="OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OpenAI API key is not configured")
        payload = {
            "model": self._model,
            "input": [{"role": m.role, "content": m.content} for m in request.messages],
            "max_output_tokens": request.max_output_tokens,
        }
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        if len(body) > 256_000:
            raise ValueError("model request body exceeds 256KB")
        http_request = Request(
            _OPENAI_RESPONSES_URL, data=body, method="POST",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            with self._opener(http_request, timeout=self._timeout) as response:
                raw = response.read(_MAX_RESPONSE_BYTES + 1)
        except HTTPError as exc:
            raise RuntimeError(f"OpenAI request failed with HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError("OpenAI request could not reach the configured endpoint") from exc
        if len(raw) > _MAX_RESPONSE_BYTES:
            raise RuntimeError("OpenAI response exceeds the configured size limit")
        try:
            document = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError("OpenAI returned an invalid JSON response") from exc
        output_text = document.get("output_text")
        if not isinstance(output_text, str) or not output_text.strip():
            raise RuntimeError("OpenAI response did not contain bounded text output")
        return ModelResponse(
            provider="openai", model=self._model, content=output_text[:20_000],
            finish_reason=document.get("status") if isinstance(document.get("status"), str) else None,
        )
