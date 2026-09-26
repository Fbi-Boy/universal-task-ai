import json
from collections.abc import Mapping

import pytest

from backend.core.model_gateway import ModelMessage, ModelRequest
from backend.core.openai_gateway import OpenAIModelGateway
from backend.core.secret_provider import SecretProvider

class FakeResponse:
    def __init__(self, payload: Mapping[str, object]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, limit: int) -> bytes:
        return self._raw[:limit]

class FakeSecrets(SecretProvider):
    def get(self, name: str, *, env_name: str | None = None, required: bool = True) -> str | None:
        assert name == "openai_api_key"
        return "test-secret"

def test_openai_gateway_uses_fixed_endpoint_and_server_side_secret() -> None:
    captured = {}
    def opener(request, *, timeout):
        captured["url"] = request.full_url
        captured["authorization"] = request.get_header("Authorization")
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse({"output_text": "hello", "status": "completed"})
    gateway = OpenAIModelGateway(FakeSecrets(), model="gpt-test", timeout_seconds=12, opener=opener)
    response = gateway.generate(ModelRequest(messages=[ModelMessage(role="user", content="hello")]))
    assert response.content == "hello"
    assert captured["url"] == "https://api.openai.com/v1/responses"
    assert captured["authorization"] == "Bearer test-secret"
    assert captured["timeout"] == 12
    assert captured["body"]["model"] == "gpt-test"

def test_openai_gateway_rejects_nonzero_temperature() -> None:
    gateway = OpenAIModelGateway(
        FakeSecrets(), model="gpt-test",
        opener=lambda *args, **kwargs: pytest.fail("network must not be reached"),
    )
    with pytest.raises(ValueError, match="temperature=0"):
        gateway.generate(ModelRequest(
            messages=[ModelMessage(role="user", content="hello")], temperature=0.5
        ))

def test_openai_gateway_does_not_accept_custom_endpoint() -> None:
    gateway = OpenAIModelGateway(FakeSecrets(), model="gpt-test")
    assert gateway._opener is not None
