from pathlib import Path

import pytest

from backend.core.audit_sink import InMemoryAuditSink
from backend.core.permissions import ToolPermission
from backend.core.planner import ExecutionPlan, PlanStep
from backend.core.schemas import TaskContract
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tool_invocation import ToolInvocation
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(name="echo", description="test echo")

    def run(self, arguments):
        return ToolResult(success=True, output=arguments.get("value", ""))


class DeniedTool(Tool):
    metadata = ToolMetadata(name="denied", description="denied test")

    def run(self, arguments):
        raise AssertionError("denied tool must never execute")


def _plan() -> ExecutionPlan:
    return ExecutionPlan(steps=[PlanStep(kind="tool", description="invoke tool")])


def _contract():
    return TaskContract(goal="echo", tools_required=["echo"])


def test_executor_runs_tool_only_through_boundary(tmp_path: Path) -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"echo"})))
    audit = InMemoryAuditSink()
    executor = TaskExecutor(SQLiteRunStateStore(tmp_path / "runs.db"), boundary, audit)
    result = executor.execute(
        _contract(), _plan(),
        tool_invocations=(ToolInvocation(tool_name="echo", arguments={"value": "ok"}),),
    )
    assert result.output == "ok"
    assert [event.event_type for event in audit.events] == [
        "task_started", "tool_authorized", "tool_started", "tool_finished", "task_finished"
    ]


def test_executor_denies_tool_and_audits_failure(tmp_path: Path) -> None:
    registry = ToolRegistry()
    registry.register(DeniedTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset()))
    audit = InMemoryAuditSink()
    executor = TaskExecutor(SQLiteRunStateStore(tmp_path / "runs.db"), boundary, audit)
    with pytest.raises(PermissionError):
        executor.execute(_contract(), _plan(), tool_invocations=(ToolInvocation(tool_name="denied"),))
    assert any(event.event_type == "tool_denied" for event in audit.events)
    assert any(event.event_type == "task_failed" for event in audit.events)
