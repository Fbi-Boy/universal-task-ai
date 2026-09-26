from pathlib import Path
from uuid import uuid4

import pytest

from backend.core.approval import ApprovalState
from backend.core.approval_store import ApprovalStore
from backend.core.audit_sink import InMemoryAuditSink
from backend.core.planner import ExecutionPlan, PlanStep
from backend.core.permissions import ToolPermission
from backend.core.schemas import TaskContract
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tool_invocation import ToolInvocation
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(name="echo", description="returns its value")

    def __init__(self) -> None:
        self.calls = 0

    def run(self, arguments):
        self.calls += 1
        return ToolResult(success=True, output=arguments["value"])


def make_plan(task_id):
    return ExecutionPlan(
        task_id=task_id,
        steps=[
            PlanStep(
                step_id="tool-1",
                kind="tool",
                objective="run the bounded tool",
                required_tools=["echo"],
            )
        ],
    )


def make_executor(tmp_path: Path, *, approvals: ApprovalStore):
    registry = ToolRegistry()
    echo = EchoTool()
    registry.register(echo)
    boundary = RuntimeToolBoundary(
        registry,
        ToolPermission(frozenset({"echo"})),
    )
    audit = InMemoryAuditSink()
    executor = TaskExecutor(
        SQLiteRunStateStore(tmp_path / "runs.sqlite3"),
        boundary,
        audit,
        approvals,
    )
    return executor, echo, audit


def test_approval_execution_persists_and_can_be_approved_once(tmp_path: Path):
    task_id = uuid4()
    plan_id = uuid4()
    invocation = ToolInvocation(tool_name="echo", arguments={"value": "hello"})
    first = ApprovalStore(tmp_path / "approvals.sqlite3")
    created = first.create_execution(
        task_id,
        "run-1",
        plan_id,
        (invocation,),
        action="execute echo",
    )
    first.approve(created.request.approval_id)

    second = ApprovalStore(tmp_path / "approvals.sqlite3")
    consumed = second.consume_execution(created.request.approval_id)

    assert consumed.request.state is ApprovalState.CONSUMED
    assert consumed.run_id == "run-1"
    assert consumed.plan_id == plan_id
    assert consumed.invocations[0] == invocation

    with pytest.raises(ValueError, match="approved or was already consumed"):
        second.consume_execution(created.request.approval_id)


def test_approval_execution_rejects_secret_bearing_arguments(tmp_path: Path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    invocation = ToolInvocation(
        tool_name="echo",
        arguments={"nested": {"token": "do-not-persist"}},
    )

    with pytest.raises(ValueError, match="secret-bearing"):
        store.create_execution(
            uuid4(),
            "run-secret",
            uuid4(),
            (invocation,),
            action="execute echo",
        )


def test_executor_waits_then_resumes_approved_tool_once(tmp_path: Path):
    approvals = ApprovalStore(tmp_path / "approvals.sqlite3")
    executor, echo, audit = make_executor(tmp_path, approvals=approvals)
    task_id = uuid4()
    contract = TaskContract(
        task_id=task_id,
        goal="execute echo",
        tools_allowed=["echo"],
        tools_required=["echo"],
        approval_required=True,
    )
    plan = make_plan(task_id)

    waiting = executor.execute(
        contract,
        plan,
        tool_invocations=(ToolInvocation(tool_name="echo", arguments={"value": "ok"}),),
    )

    assert waiting.status.value == "waiting_approval"
    assert waiting.approval_id
    assert echo.calls == 0

    approvals.approve(uuid4()) if False else None
    approvals.approve(__import__("uuid").UUID(waiting.approval_id))

    resumed = executor.resume_approved(
        contract,
        plan,
        run_id=waiting.run_id,
        approval_id=waiting.approval_id,
        actor_id="test-operator",
    )

    assert resumed.status.value == "succeeded"
    assert resumed.output == "ok"
    assert echo.calls == 1
    assert approvals.get(__import__("uuid").UUID(waiting.approval_id)).state is ApprovalState.CONSUMED

    with pytest.raises(ValueError, match="not waiting for approval"):
        executor.resume_approved(
            contract,
            plan,
            run_id=waiting.run_id,
            approval_id=waiting.approval_id,
            actor_id="test-operator",
        )

    assert echo.calls == 1
    assert any(event.event_type == "tool_started" for event in audit.events)


def test_missing_approval_store_fails_closed_for_approval_required_tools(tmp_path: Path):
    registry = ToolRegistry()
    registry.register(EchoTool())
    boundary = RuntimeToolBoundary(
        registry,
        ToolPermission(frozenset({"echo"})),
    )
    executor = TaskExecutor(
        SQLiteRunStateStore(tmp_path / "runs.sqlite3"),
        boundary,
    )
    task_id = uuid4()
    contract = TaskContract(
        task_id=task_id,
        goal="execute echo",
        tools_allowed=["echo"],
        tools_required=["echo"],
        approval_required=True,
    )

    with pytest.raises(RuntimeError, match="durable approval store"):
        executor.execute(
            contract,
            make_plan(task_id),
            tool_invocations=(ToolInvocation(tool_name="echo", arguments={"value": "x"}),),
        )
