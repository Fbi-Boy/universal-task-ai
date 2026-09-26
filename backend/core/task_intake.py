from dataclasses import dataclass
from uuid import uuid4
from backend.core.analyzer import TaskAnalysis
from backend.core.schemas import TaskContract

@dataclass(frozen=True)
class TaskIntakeResult:
    analysis: TaskAnalysis
    contract: TaskContract

class TaskIntakeService:
    def intake(self, task_text: str) -> TaskIntakeResult:
        analysis = TaskAnalysis.from_task_text(task_text)
        contract = TaskContract(task_id=uuid4(), goal=analysis.normalized_goal, constraints=list(analysis.requirements))
        return TaskIntakeResult(analysis=analysis, contract=contract)
