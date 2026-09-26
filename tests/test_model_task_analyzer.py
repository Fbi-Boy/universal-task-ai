import pytest

from backend.core.model_gateway import ModelMessage, ModelRequest, ModelResponse, StaticModelGateway
from backend.core.model_task_analyzer import ModelTaskAnalyzer


def test_model_task_analyzer_accepts_strict_json() -> None:
    gateway = StaticModelGateway(
        '{"normalized_goal":"build a flowchart","requirements":["use Mermaid"],'
        '"ambiguity_level":"low","ambiguity_reasons":[],"assumptions":[],'
        '"needs_clarification":false}'
    )
    result = ModelTaskAnalyzer(gateway).analyze("build a flowchart")
    assert result.normalized_goal == "build a flowchart"
    assert result.requirements == ["use Mermaid"]


def test_model_task_analyzer_rejects_extra_model_fields() -> None:
    gateway = StaticModelGateway(
        '{"normalized_goal":"x","requirements":[],"ambiguity_level":"low",'
        '"ambiguity_reasons":[],"assumptions":[],"needs_clarification":false,'
        '"tools_allowed":["browser"]}'
    )
    with pytest.raises(ValueError):
        ModelTaskAnalyzer(gateway).analyze("x")


def test_model_task_analyzer_rejects_non_json_model_output() -> None:
    gateway = StaticModelGateway("I will do it.")
    with pytest.raises(ValueError, match="valid JSON"):
        ModelTaskAnalyzer(gateway).analyze("x")


def test_model_task_analyzer_does_not_allow_model_to_change_runtime_request() -> None:
    class RecordingGateway:
        def __init__(self) -> None:
            self.request = None

        def generate(self, request: ModelRequest) -> ModelResponse:
            self.request = request
            return ModelResponse(
                provider="test",
                model="test",
                content='{"normalized_goal":"x","requirements":[],"ambiguity_level":"low",'
                        '"ambiguity_reasons":[],"assumptions":[],"needs_clarification":false}',
            )

    gateway = RecordingGateway()
    result = ModelTaskAnalyzer(gateway).analyze("x")
    assert result.normalized_goal == "x"
    assert gateway.request is not None
    assert all("permission" not in message.content.lower() for message in gateway.request.messages)
