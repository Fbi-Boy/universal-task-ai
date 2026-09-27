from backend.core.analyzer import TaskAnalysis
from backend.core.task_intake import TaskIntakeService


class FakeAnalyzer:
    def analyze(self, task_text: str) -> TaskAnalysis:
        return TaskAnalysis(
            normalized_goal=task_text.strip(),
            requirements=["bounded output"],
            ambiguity_level="low",
        )


def test_task_intake_can_use_injected_analyzer() -> None:
    result = TaskIntakeService(FakeAnalyzer()).intake("build an ERD")
    assert result.analysis.requirements == ["bounded output"]
    assert result.contract.goal == "build an ERD"
    assert result.contract.constraints == ["bounded output"]
