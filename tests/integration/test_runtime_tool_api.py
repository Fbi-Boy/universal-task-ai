from pathlib import Path

import pytest

from backend.core.audit_sink import InMemoryAuditSink
from backend.core.approval_store import ApprovalStore
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner
from backend.core.task_service import TaskService
from backend.core.tool_invocation import ToolInvocation
from backend.core.runtime_tools import build_runtime_tool_boundary


def make_service(tmp_path: Path) -> TaskService:
    executor = TaskExecutor(
        SQLiteRunStateStore(tmp_path / "runs.sqlite3"),
        build_runtime_tool_boundary(),
        InMemoryAuditSink(),
        ApprovalStore(tmp_path / "approvals.sqlite3"),
    )
    return TaskService(TaskIntakeService(), TaskPlanner(), executor)


def test_calculator_invocation_runs_through_runtime_boundary(tmp_path: Path):
    service = make_service(tmp_path)

    result = service.run(
        "calculate the expression",
        tool_invocations=(ToolInvocation(tool_name="calculator", arguments={"expression": "2 + 3 * 4"}),),
    )

    assert result.execution.status.value == "succeeded"
    assert result.execution.output == "14"


def test_unknown_tool_fails_closed(tmp_path: Path):
    service = make_service(tmp_path)

    with pytest.raises(PermissionError, match="tool is not registered"):
        service.run(
            "run a tool",
            tool_invocations=(ToolInvocation(tool_name="not-registered", arguments={}),),
        )


def test_task_service_bounds_tool_invocation_count(tmp_path: Path):
    service = make_service(tmp_path)
    invocations = tuple(
        ToolInvocation(tool_name="calculator", arguments={"expression": "1 + 1"})
        for _ in range(9)
    )

    with pytest.raises(ValueError, match="at most 8"):
        service.run("run bounded tools", tool_invocations=invocations)
