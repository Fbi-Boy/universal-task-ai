from dataclasses import dataclass
from backend.core.task_executor import ExecutionResult, TaskExecutor
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner

@dataclass(frozen=True)
class TaskRunResult:
    intake: object
    execution: ExecutionResult

class TaskService:
    """Application service connecting intake, planning, execution, and resume."""
    def __init__(self, intake: TaskIntakeService, planner: TaskPlanner, executor: TaskExecutor) -> None:
        self._intake = intake
        self._planner = planner
        self._executor = executor

    def run(self, task_text: str) -> TaskRunResult:
        intake = self._intake.intake(task_text)
        plan = self._planner.plan(intake.contract)
        execution = self._executor.execute(intake.contract, plan)
        return TaskRunResult(intake=intake, execution=execution)

    def resume_approved(self, *, run_id: str, approval_id: str, actor_id: str) -> ExecutionResult:
        return self._executor.resume_approved_from_run(
            run_id=run_id,
            approval_id=approval_id,
            actor_id=actor_id,
        )
