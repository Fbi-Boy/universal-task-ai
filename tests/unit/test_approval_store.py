from uuid import uuid4

import pytest

from backend.core.approval_store import ApprovalStore
from backend.core.tool_invocation import ToolInvocation


def test_reject_only_updates_pending_state(tmp_path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    request = store.create(uuid4(), "publish")
    rejected = store.reject(request.approval_id)
    assert rejected.state.value == "rejected"
    with pytest.raises(ValueError, match="pending approvals"):
        store.reject(request.approval_id)


def test_approval_execution_rejects_secret_arguments(tmp_path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    with pytest.raises(ValueError, match="secret-bearing"):
        store.create_execution(
            uuid4(),
            "run-1",
            uuid4(),
            (ToolInvocation(tool_name="echo", arguments={"token": "secret"}),),
            action="execute tool",
        )


def test_approval_execution_consumption_is_atomic(tmp_path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    task_id = uuid4()
    plan_id = uuid4()
    created = store.create_execution(
        task_id,
        "run-1",
        plan_id,
        (ToolInvocation(tool_name="echo", arguments={"value": "ok"}),),
        action="execute tool",
    )
    store.approve(created.request.approval_id)
    consumed = store.consume_execution(created.request.approval_id)
    assert consumed.run_id == "run-1"
    with pytest.raises(ValueError, match="not approved or was already consumed"):
        store.consume_execution(created.request.approval_id)
