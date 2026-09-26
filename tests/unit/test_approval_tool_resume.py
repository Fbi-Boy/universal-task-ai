from pathlib import Path
from uuid import uuid4

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


class ApprovalTool(Tool):
    metadata = ToolMetadata(
        name="message.send",
        description="test side effect",
        requires_approval=True,
    )

    calls = 0

    def run(self, arguments):
        type(self).calls += 1
        return ToolResult(success=True, output=arguments["value"])


def _contract():
    return TaskContract(task_id=uuid4(), goal="send", tools_required=["message.send"])


def _plan(task_id):
    return ExecutionPlan(
        task_id=task_id,
        steps=[PlanStep(step_id="tool-1", kind="tool", objective="send")],
    )


def _executor(tmp_path: Path):
    registry = ToolRegistry()
    registry.register(ApprovalTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"message.send"})))
    audit = InMemoryAuditSink()
    return TaskExecutor(SQLiteRunStateStore(tmp_path / "runs.db"), boundary, audit), audit


def test_approval_required_persists_pending_state_without_running_tool(tmp_path: Path):
    ApprovalTool.calls = 0
    executor, audit = _executor(tmp_path)
    contract = _contract()
    invocation = ToolInvocation(tool_name="message.send", arguments={"value": "ok"})

    result = executor.execute(contract, _plan(contract.task_id), tool_invocations=(invocation,))

    assert result.status.value == "waiting_approval"
    assert result.approval_id
    assert ApprovalTool.calls == 0
    state = executor._store.get(result.run_id)
    assert state is not None
    assert state.status == "waiting_approval"
    assert "arguments_sha256" in state.payload
    assert '"value"' not in state.payload
    assert not any(event.event_type == "tool_started" for event in audit.events)


def test_approved_resume_executes_once_and_rejects_replay(tmp_path: Path):
    ApprovalTool.calls = 0
    executor, audit = _executor(tmp_path)
    contract = _contract()
    plan = _plan(contract.task_id)
    invocation = ToolInvocation(tool_name="message.send", arguments={"value": "ok"})
    pending = executor.execute(contract, plan, tool_invocations=(invocation,))

    result = executor.resume_approved(
        pending.run_id, pending.approval_id or "", invocation, "operator-1"
    )

    assert result.status.value == "succeeded"
    assert result.output == "ok"
    assert ApprovalTool.calls == 1
    assert any(event.actor == "operator-1" for event in audit.events if event.event_type == "tool_started")

    with pytest.raises(ValueError, match="not waiting"):
        executor.resume_approved(
            pending.run_id, pending.approval_id or "", invocation, "operator-1"
        )
    assert ApprovalTool.calls == 1


def test_approval_resume_rejects_changed_arguments(tmp_path: Path):
    executor, _ = _executor(tmp_path)
    contract = _contract()
    pending = executor.execute(
        contract,
        _plan(contract.task_id),
        tool_invocations=(ToolInvocation(tool_name="message.send", arguments={"value": "ok"}),),
    )

    with pytest.raises(ValueError, match="arguments do not match"):
        executor.resume_approved(
            pending.run_id,
            pending.approval_id or "",
            ToolInvocation(tool_name="message.send", arguments={"value": "tampered"}),
            "operator-1",
        )
