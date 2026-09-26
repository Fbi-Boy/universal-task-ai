from pathlib import Path
from uuid import UUID, uuid4

import pytest

from backend.core.approval_store import ApprovalStore
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


def _plan(task_id):
    return ExecutionPlan(
        task_id=task_id,
        steps=[PlanStep(step_id="tool-1", kind="tool", objective="invoke tool")],
    )


def test_approval_store_bounds_execution_manifest(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.db")
    invocations = tuple(
        ToolInvocation(tool_name="echo", arguments={"value": str(i)})
        for i in range(9)
    )
    with pytest.raises(ValueError, match="at most 8"):
        store.create_execution(
            uuid4(),
            "run-1",
            uuid4(),
            invocations,
            action="execute",
        )


def test_resume_preserves_durable_manifest_and_records_actor(tmp_path: Path) -> None:
    task_id = uuid4()
    contract = TaskContract(
        task_id=task_id,
        goal="echo",
        tools_required=["echo"],
        approval_required=True,
    )
    registry = ToolRegistry()
    registry.register(EchoTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"echo"})))
    audit = InMemoryAuditSink()
    approvals = ApprovalStore(tmp_path / "approvals.db")
    runs = SQLiteRunStateStore(tmp_path / "runs.db")
    executor = TaskExecutor(runs, boundary, audit, approvals)

    waiting = executor.execute(
        contract,
        _plan(task_id),
        tool_invocations=(ToolInvocation(tool_name="echo", arguments={"value": "ok"}),),
    )
    state = runs.get(waiting.run_id)
    assert state is not None
    assert state.status == "waiting_approval"
    assert "contract" in state.payload
    assert "plan" in state.payload
    assert waiting.approval_id is not None

    approvals.approve(UUID(waiting.approval_id))
    result = executor.resume_approved_from_run(
        run_id=waiting.run_id,
        approval_id=waiting.approval_id,
        actor_id="human-operator",
    )
    assert result.status.value == "succeeded"
    consumed = [event for event in audit.events if event.event_type == "approval_consumed"]
    assert len(consumed) == 1
    assert consumed[0].actor == "human-operator"
