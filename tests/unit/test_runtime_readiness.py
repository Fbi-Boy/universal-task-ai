from pathlib import Path

import pytest

from backend.core.approval_store import ApprovalStore
from backend.core.audit_sink import SQLiteAuditSink
from backend.core.permissions import ToolPermission
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tools import ToolRegistry


def _executor(tmp_path: Path) -> TaskExecutor:
    return TaskExecutor(
        SQLiteRunStateStore(tmp_path / "runs.sqlite3"),
        RuntimeToolBoundary(ToolRegistry(), ToolPermission(frozenset())),
        SQLiteAuditSink(tmp_path / "audit.sqlite3"),
        ApprovalStore(tmp_path / "approvals.sqlite3"),
    )


def test_runtime_readiness_probes_all_durable_dependencies(tmp_path: Path) -> None:
    assert _executor(tmp_path).readiness() == {
        "run_state": "ok",
        "approval_store": "ok",
        "audit_sink": "ok",
    }


def test_runtime_readiness_fails_closed_without_approval_store(tmp_path: Path) -> None:
    executor = TaskExecutor(
        SQLiteRunStateStore(tmp_path / "runs.sqlite3"),
        RuntimeToolBoundary(ToolRegistry(), ToolPermission(frozenset())),
        SQLiteAuditSink(tmp_path / "audit.sqlite3"),
        None,
    )
    with pytest.raises(RuntimeError, match="approval store"):
        executor.readiness()
