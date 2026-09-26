from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4

from backend.core.analyzer import TaskAnalysis, TaskAnalysis as DeterministicTaskAnalysis
from backend.core.schemas import TaskContract


class TaskAnalyzer(Protocol):
    def analyze(self, task_text: str) -> TaskAnalysis: ...


@dataclass(frozen=True)
class TaskIntakeResult:
    analysis: TaskAnalysis
    contract: TaskContract


class TaskIntakeService:
    def __init__(self, analyzer: TaskAnalyzer | None = None) -> None:
        self._analyzer = analyzer

    def intake(self, task_text: str) -> TaskIntakeResult:
        analysis = (
            self._analyzer.analyze(task_text)
            if self._analyzer is not None
            else DeterministicTaskAnalysis.from_task_text(task_text)
        )
        contract = TaskContract(
            task_id=uuid4(),
            goal=analysis.normalized_goal,
            constraints=list(analysis.requirements),
        )
        return TaskIntakeResult(analysis=analysis, contract=contract)
