import pytest
from backend.core.model_gateway import ModelMessage, ModelRequest, StaticModelGateway

def test_model_message_rejects_extra_fields() -> None:
    with pytest.raises(ValueError):
        ModelMessage(role="user", content="hello", secret="nope")

def test_model_request_enforces_total_content_bound() -> None:
    request = ModelRequest(messages=[ModelMessage(role="user", content="x" * 16_000) for _ in range(7)])
    with pytest.raises(ValueError, match="100000"):
        request.validate_bounds()

def test_static_gateway_is_deterministic_and_offline() -> None:
    gateway = StaticModelGateway("approved")
    request = ModelRequest(messages=[ModelMessage(role="user", content="task")])
    first = gateway.generate(request)
    second = gateway.generate(request)
    assert first == second
    assert first.provider == "static"
    assert first.content == "approved"
