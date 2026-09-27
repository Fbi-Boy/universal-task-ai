from pathlib import Path
from uuid import uuid4

from backend.core.approval import ApprovalState
from backend.core.approval_store import ApprovalStore
from backend.core.tool_invocation import ToolInvocation


def test_approval_decision_requires_actor_and_persists_metadata(tmp_path: Path):
    db = tmp_path / "approvals.sqlite3"
    task_id = uuid4()
    store = ApprovalStore(db)
    execution = store.create_execution(
        task_id,
        "run-1",
        uuid4(),
        (ToolInvocation(tool_name="calculator", arguments={"a": 1}),),
        action="execute calculator",
    )

    approved = store.approve(execution.request.approval_id, "operator-1")
    assert approved.state is ApprovalState.APPROVED

    info = store.get_execution_info(execution.request.approval_id)
    assert info is not None
    assert info.state is ApprovalState.APPROVED
    assert info.decided_by == "operator-1"
    assert info.decided_at


def test_approval_reject_persists_actor_and_cannot_be_reused(tmp_path: Path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    request = store.create(uuid4(), "delete file")

    rejected = store.reject(request.approval_id, "operator-2")
    assert rejected.state is ApprovalState.REJECTED

    try:
        store.reject(request.approval_id, "operator-2")
    except ValueError as exc:
        assert "only pending approvals" in str(exc)
    else:
        raise AssertionError("rejected approval was reusable")


def test_approval_decision_actor_is_bounded(tmp_path: Path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    request = store.create(uuid4(), "run tool")

    try:
        store.approve(request.approval_id, " ")
    except ValueError as exc:
        assert "actor_id" in str(exc)
    else:
        raise AssertionError("blank actor was accepted")

    try:
        store.approve(request.approval_id, "x" * 129)
    except ValueError as exc:
        assert "at most 128" in str(exc)
    else:
        raise AssertionError("oversized actor was accepted")


def test_decision_columns_migrate_existing_database(tmp_path: Path):
    import sqlite3

    db = tmp_path / "legacy.sqlite3"
    conn = sqlite3.connect(db)
    conn.execute(
        "CREATE TABLE approvals (approval_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, action TEXT NOT NULL, state TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()

    store = ApprovalStore(db)
    request = store.create(uuid4(), "legacy decision")
    store.approve(request.approval_id, "operator-legacy")

    info = store.get(request.approval_id)
    assert info is not None
