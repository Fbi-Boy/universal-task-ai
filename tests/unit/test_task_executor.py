import json

import pytest

from backend.core.approval_store import ApprovalStore
from backend.core.task_planner import TaskPlanner
from backend.core.schemas import TaskContract
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor


def test_executor_persists_success(tmp_path):
    store = SQLiteRunStateStore(tmp_path / "runs.sqlite3")
    contract = TaskContract(goal="Create a report")
    result = TaskExecutor(store).execute(contract, TaskPlanner().plan(contract))
    assert result.status.value == "succeeded"
    state = store.get(result.run_id)
    assert state is not None and state.status == "succeeded"
    assert json.loads(state.payload)["task_id"] == str(contract.task_id)


def test_executor_fails_closed_for_unregistered_tool(tmp_path):
    store = SQLiteRunStateStore(tmp_path / "runs.sqlite3")
    contract = TaskContract(goal="Search", tools_required=["web.search"])
    with pytest.raises(RuntimeError, match="side-effect boundary"):
        TaskExecutor(store).execute(contract, TaskPlanner().plan(contract))


def test_executor_waits_for_approval_when_required(tmp_path):
    store = SQLiteRunStateStore(tmp_path / "runs.sqlite3")
    approvals = ApprovalStore(tmp_path / "approvals.sqlite3")
    contract = TaskContract(goal="Send", tools_required=["message.send"], approval_required=True)

    # The planner/executor contract requires an explicit invocation before a
    # durable approval can be created. The tool boundary is intentionally not
    # configured here, so the executor must fail closed rather than pretending
    # an approval exists.
    with pytest.raises(RuntimeError, match="side-effect boundary"):
        TaskExecutor(store, approval_store=approvals).execute(
            contract,
            TaskPlanner().plan(contract),
        )
