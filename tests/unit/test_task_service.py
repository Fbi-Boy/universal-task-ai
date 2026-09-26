from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner
from backend.core.task_service import TaskService

def test_task_service_connects_intake_planning_and_execution(tmp_path):
    service = TaskService(TaskIntakeService(), TaskPlanner(), TaskExecutor(SQLiteRunStateStore(tmp_path / "runs.sqlite3")))
    result = service.run("Create a report")
    assert result.execution.status.value == "succeeded"
    assert result.intake.contract.goal == "Create a report"
