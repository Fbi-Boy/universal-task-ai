from pathlib import Path
from uuid import uuid4

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


class DeniedTool(Tool):
    metadata = ToolMetadata(name="denied", description="denied test")

    def run(self, arguments):
        raise AssertionError("denied tool must never execute")


class FailingTool(Tool):
    metadata = ToolMetadata(name="failing", description="failing test")

    def run(self, arguments):
        raise ValueError("tool failure")


def _contract():
    return TaskContract(task_id=uuid4(), goal="echo", tools_required=["echo"])


def _plan(task_id):
    return ExecutionPlan(
        task_id=task_id,
        steps=[
            PlanStep(
                step_id="tool-1",
                kind="tool",
                objective="invoke tool",
            )
        ],
    )


def test_executor_runs_tool_only_through_boundary(tmp_path: Path) -> None:
    contract = _contract()
    registry = ToolRegistry()
    registry.register(EchoTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"echo"})))
    audit = InMemoryAuditSink()
    executor = TaskExecutor(SQLiteRunStateStore(tmp_path / "runs.db"), boundary, audit)
    result = executor.execute(
        contract,
        _plan(contract.task_id),
        tool_invocations=(ToolInvocation(tool_name="echo", arguments={"value": "ok"}),),
    )
    assert result.output == "ok"
    assert [event.event_type for event in audit.events] == [
        "task_started",
        "tool_authorized",
        "tool_started",
        "tool_finished",
        "task_finished",
    ]


def test_executor_denies_tool_and_audits_failure(tmp_path: Path) -> None:
    contract = _contract()
    registry = ToolRegistry()
    registry.register(DeniedTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset()))
    audit = InMemoryAuditSink()
    executor = TaskExecutor(SQLiteRunStateStore(tmp_path / "runs.db"), boundary, audit)
    with pytest.raises(PermissionError):
        executor.execute(
            contract,
            _plan(contract.task_id),
            tool_invocations=(ToolInvocation(tool_name="denied"),),
        )
    assert any(event.event_type == "tool_denied" for event in audit.events)
    assert any(event.event_type == "task_failed" for event in audit.events)
    assert not any(event.event_type == "tool_authorized" for event in audit.events)


def test_executor_waits_for_approval_before_tool_execution(tmp_path: Path) -> None:
    contract = _contract().model_copy(update={"approval_required": True})
    registry = ToolRegistry()
    registry.register(DeniedTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"denied"})))
    audit = InMemoryAuditSink()
    approvals = ApprovalStore(tmp_path / "approvals.db")
    executor = TaskExecutor(
        SQLiteRunStateStore(tmp_path / "runs.db"),
        boundary,
        audit,
        approvals,
    )
    result = executor.execute(
        contract,
        _plan(contract.task_id),
        tool_invocations=(ToolInvocation(tool_name="denied"),),
    )
    assert result.status.value == "waiting_approval"
    assert result.approval_id is not None
    assert not any(event.event_type == "tool_started" for event in audit.events)


def test_approved_tool_executes_once_and_duplicate_resume_is_rejected(tmp_path: Path) -> None:
    contract = _contract().model_copy(update={"approval_required": True})
    registry = ToolRegistry()
    calls = {"count": 0}

    class CountingTool(EchoTool):
        def run(self, arguments):
            calls["count"] += 1
            return super().run(arguments)

    registry.register(CountingTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"echo"})))
    approvals = ApprovalStore(tmp_path / "approvals.db")
    executor = TaskExecutor(
        SQLiteRunStateStore(tmp_path / "runs.db"),
        boundary,
        InMemoryAuditSink(),
        approvals,
    )
    waiting = executor.execute(
        contract,
        _plan(contract.task_id),
        tool_invocations=(ToolInvocation(tool_name="echo", arguments={"value": "approved"}),),
    )
    approvals.approve(uuid4()) if False else None
    approvals.approve(__import__("uuid").UUID(waiting.approval_id))
    resumed = executor.resume_approved(
        contract,
        _plan(contract.task_id),
        run_id=waiting.run_id,
        approval_id=waiting.approval_id,
        actor_id="test-user",
    )
    assert resumed.status.value == "succeeded"
    assert resumed.output == "approved"
    assert calls["count"] == 1

    with pytest.raises(ValueError, match="run is not waiting for approval"):
        executor.resume_approved(
            contract,
            _plan(contract.task_id),
            run_id=waiting.run_id,
            approval_id=waiting.approval_id,
            actor_id="test-user",
        )


def test_tool_failure_is_not_a_boundary_denial(tmp_path: Path) -> None:
    contract = _contract().model_copy(update={"tools_required": ["failing"]})
    registry = ToolRegistry()
    registry.register(FailingTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"failing"})))
    audit = InMemoryAuditSink()
    executor = TaskExecutor(SQLiteRunStateStore(tmp_path / "runs.db"), boundary, audit)
    with pytest.raises(ValueError, match="tool failure"):
        executor.execute(contract, _plan(contract.task_id), tool_invocations=(ToolInvocation(tool_name="failing"),))
    assert not any(event.event_type == "tool_denied" for event in audit.events)
    assert any(event.event_type == "tool_finished" and event.success is False for event in audit.events)
