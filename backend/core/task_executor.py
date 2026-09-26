import json
from dataclasses import dataclass
from uuid import uuid4

from backend.core.planner import ExecutionPlan
from backend.core.run_lifecycle import RunStatus, transition
from backend.core.schemas import TaskContract
from backend.core.state_store import RunState, SQLiteRunStateStore

@dataclass(frozen=True)
class ExecutionResult:
    run_id: str
    status: RunStatus
    output: str
    plan: ExecutionPlan

class TaskExecutor:
    """Executes only the currently supported, side-effect-free runtime stages."""
    def __init__(self, store: SQLiteRunStateStore) -> None:
        self._store = store

    def execute(self, contract: TaskContract, plan: ExecutionPlan) -> ExecutionResult:
        run_id = str(uuid4())
        status = RunStatus.CREATED
        self._store.save(RunState(run_id, status.value, json.dumps({"task_id": str(contract.task_id)})))
        status = transition(status, RunStatus.RUNNING)
        self._store.save(RunState(run_id, status.value, json.dumps({"task_id": str(contract.task_id), "plan_id": str(plan.plan_id)})))
        try:
            if any(step.kind in {"tool", "agent"} for step in plan.steps):
                if contract.approval_required:
                    status = transition(status, RunStatus.WAITING_APPROVAL)
                    self._store.save(RunState(run_id, status.value, json.dumps({"task_id": str(contract.task_id), "plan_id": str(plan.plan_id), "reason": "execution boundary requires approval"})))
                    return ExecutionResult(run_id, status, "Execution is waiting for approval.", plan)
                raise RuntimeError("execution requires a registered side-effect boundary")
            status = transition(status, RunStatus.SUCCEEDED)
            output = "Task contract validated and execution completed through the safe baseline runtime. No external tools or side effects were invoked."
            self._store.save(RunState(run_id, status.value, json.dumps({"task_id": str(contract.task_id), "plan_id": str(plan.plan_id), "output": output})))
            return ExecutionResult(run_id, status, output, plan)
        except Exception as exc:
            if status == RunStatus.RUNNING:
                status = transition(status, RunStatus.FAILED)
            self._store.save(RunState(run_id, status.value, json.dumps({"task_id": str(contract.task_id), "plan_id": str(plan.plan_id), "error": str(exc)[:500]})))
            raise
