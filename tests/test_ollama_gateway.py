import json
from collections.abc import Mapping

import pytest

from backend.core.model_gateway import ModelMessage, ModelRequest
from backend.core.ollama_gateway import OllamaModelGateway


class FakeResponse:
    def __init__(self, payload: Mapping[str, object]) -> None:
        self._raw = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, limit: int) -> bytes:
        return self._raw[:limit]


def test_ollama_gateway_is_loopback_only() -> None:
    with pytest.raises(ValueError):
        OllamaModelGateway(model="local", base_url="http://example.com")


def test_ollama_gateway_uses_local_endpoint() -> None:
    captured = {}

    def opener(request, *, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode())
        return FakeResponse({"message": {"content": "hello"}, "done": True})

    gateway = OllamaModelGateway(model="local", timeout_seconds=7, opener=opener)
    response = gateway.generate(
        ModelRequest(messages=[ModelMessage(role="user", content="hello")])
    )
    assert response.content == "hello"
    assert captured["url"] == "http://127.0.0.1:11434/api/chat"
    assert captured["timeout"] == 7
    assert captured["body"]["stream"] is False


def test_ollama_gateway_rejects_nonzero_temperature() -> None:
    gateway = OllamaModelGateway(model="local", opener=lambda *a, **k: pytest.fail("network"))
    with pytest.raises(ValueError, match="temperature=0"):
        gateway.generate(
            ModelRequest(
                messages=[ModelMessage(role="user", content="hello")],
                temperature=0.5,
            )
        )
