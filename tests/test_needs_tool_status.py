from pathlib import Path

from backend.core.audit_sink import InMemoryAuditSink
from backend.core.run_lifecycle import RunStatus, can_transition, transition
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner


def test_running_task_can_end_as_needs_tool_and_status_is_terminal():
    assert transition(RunStatus.RUNNING, RunStatus.NEEDS_TOOL) is RunStatus.NEEDS_TOOL
    assert not can_transition(RunStatus.NEEDS_TOOL, RunStatus.RUNNING)
    assert not can_transition(RunStatus.NEEDS_TOOL, RunStatus.SUCCEEDED)


def test_unsupported_task_is_not_reported_as_success(tmp_path: Path):
    intake = TaskIntakeService().intake("Summarize the attached document")
    contract = intake.contract
    plan = TaskPlanner().plan(contract)
    store = SQLiteRunStateStore(tmp_path / "runs.sqlite3")
    audit = InMemoryAuditSink()
    executor = TaskExecutor(store, audit_sink=audit)

    result = executor.execute(contract, plan)

    assert result.status is RunStatus.NEEDS_TOOL
    assert "was not executed" in result.output
    assert "No external action was taken" in result.output
    assert "completed" not in result.output.lower()
    persisted = store.get(result.run_id)
    assert persisted is not None
    assert persisted.status == RunStatus.NEEDS_TOOL.value
    assert any(event.event_type == "task_needs_tool" for event in audit.events)
    assert not any(event.event_type == "task_finished" and event.success is True for event in audit.events)
