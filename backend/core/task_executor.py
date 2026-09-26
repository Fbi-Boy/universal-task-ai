import json
from dataclasses import dataclass
from uuid import UUID, uuid4

from backend.core.audit import AuditEvent
from backend.core.audit_sink import AuditSink
from backend.core.planner import ExecutionPlan
from backend.core.run_lifecycle import RunStatus, transition
from backend.core.schemas import TaskContract
from backend.core.state_store import RunState, SQLiteRunStateStore
from backend.core.tool_boundary import RuntimeToolBoundary, ToolBoundaryDenied
from backend.core.tool_invocation import ToolInvocation


@dataclass(frozen=True)
class ExecutionResult:
    run_id: str
    status: RunStatus
    output: str
    plan: ExecutionPlan


class TaskExecutor:
    """Execute safe stages and explicitly bounded registered tool invocations."""

    def __init__(
        self,
        store: SQLiteRunStateStore,
        tool_boundary: RuntimeToolBoundary | None = None,
        audit_sink: AuditSink | None = None,
    ) -> None:
        self._store = store
        self._tool_boundary = tool_boundary
        self._audit = audit_sink

    def _audit_event(
        self,
        event_type: str,
        task_id: UUID,
        *,
        run_id: str,
        tool_name: str | None = None,
        success: bool | None = None,
        metadata: dict | None = None,
    ) -> None:
        if self._audit is None:
            return
        self._audit.append(
            AuditEvent(
                event_type=event_type,
                task_id=task_id,
                tool_name=tool_name,
                success=success,
                metadata={"run_id": run_id, **(metadata or {})},
            )
        )

    def execute(
        self,
        contract: TaskContract,
        plan: ExecutionPlan,
        *,
        tool_invocations: tuple[ToolInvocation, ...] = (),
    ) -> ExecutionResult:
        run_id = str(uuid4())
        status = RunStatus.CREATED
        self._store.save(
            RunState(run_id, status.value, json.dumps({"task_id": str(contract.task_id)}))
        )
        self._audit_event("task_started", contract.task_id, run_id=run_id)
        status = transition(status, RunStatus.RUNNING)
        self._store.save(
            RunState(
                run_id,
                status.value,
                json.dumps({"task_id": str(contract.task_id), "plan_id": str(plan.plan_id)}),
            )
        )
        try:
            has_tool_stage = any(step.kind == "tool" for step in plan.steps)
            has_agent_stage = any(step.kind == "agent" for step in plan.steps)

            if has_agent_stage:
                raise RuntimeError("agent execution requires a registered side-effect boundary")

            if has_tool_stage and contract.approval_required:
                status = transition(status, RunStatus.WAITING_APPROVAL)
                self._store.save(
                    RunState(
                        run_id,
                        status.value,
                        json.dumps(
                            {
                                "task_id": str(contract.task_id),
                                "plan_id": str(plan.plan_id),
                                "reason": "execution boundary requires approval",
                            }
                        ),
                    )
                )
                return ExecutionResult(run_id, status, "Execution is waiting for approval.", plan)

            if has_tool_stage:
                if self._tool_boundary is None:
                    raise RuntimeError("tool execution requires a configured side-effect boundary")
                if not tool_invocations:
                    raise RuntimeError("tool plan requires at least one explicit tool invocation")

                outputs: list[str] = []
                for invocation in tool_invocations:
                    invocation.validate_bounds()
                    try:
                        authorized_tool = self._tool_boundary.authorize(invocation.tool_name)
                    except (ToolBoundaryDenied, PermissionError, ValueError) as exc:
                        self._audit_event(
                            "tool_denied",
                            contract.task_id,
                            run_id=run_id,
                            tool_name=invocation.tool_name,
                            success=False,
                            metadata={"reason": str(exc)[:200]},
                        )
                        raise
                    self._audit_event(
                        "tool_authorized",
                        contract.task_id,
                        run_id=run_id,
                        tool_name=invocation.tool_name,
                    )
                    self._audit_event(
                        "tool_started",
                        contract.task_id,
                        run_id=run_id,
                        tool_name=invocation.tool_name,
                    )
                    try:
                        result = self._tool_boundary.execute_authorized(
                            authorized_tool,
                            invocation.arguments,
                        )
                    except Exception as exc:
                        self._audit_event(
                            "tool_finished",
                            contract.task_id,
                            run_id=run_id,
                            tool_name=invocation.tool_name,
                            success=False,
                            metadata={"error": str(exc)[:200]},
                        )
                        raise

                    self._audit_event(
                        "tool_finished",
                        contract.task_id,
                        run_id=run_id,
                        tool_name=invocation.tool_name,
                        success=result.success,
                    )
                    if not result.success:
                        raise RuntimeError(result.error or "tool execution failed")
                    outputs.append(str(result.output))

                status = transition(status, RunStatus.SUCCEEDED)
                output = "\n".join(outputs)
                self._store.save(
                    RunState(
                        run_id,
                        status.value,
                        json.dumps(
                            {
                                "task_id": str(contract.task_id),
                                "plan_id": str(plan.plan_id),
                                "output": output,
                            }
                        ),
                    )
                )
                self._audit_event("task_finished", contract.task_id, run_id=run_id, success=True)
                return ExecutionResult(run_id, status, output, plan)

            if contract.approval_required:
                status = transition(status, RunStatus.WAITING_APPROVAL)
                self._store.save(
                    RunState(
                        run_id,
                        status.value,
                        json.dumps(
                            {
                                "task_id": str(contract.task_id),
                                "plan_id": str(plan.plan_id),
                                "reason": "execution boundary requires approval",
                            }
                        ),
                    )
                )
                return ExecutionResult(run_id, status, "Execution is waiting for approval.", plan)

            status = transition(status, RunStatus.SUCCEEDED)
            output = (
                "Task contract validated and execution completed through the safe baseline runtime. "
                "No external tools or side effects were invoked."
            )
            self._store.save(
                RunState(
                    run_id,
                    status.value,
                    json.dumps(
                        {
                            "task_id": str(contract.task_id),
                            "plan_id": str(plan.plan_id),
                            "output": output,
                        }
                    ),
                )
            )
            self._audit_event("task_finished", contract.task_id, run_id=run_id, success=True)
            return ExecutionResult(run_id, status, output, plan)
        except Exception as exc:
            if status == RunStatus.RUNNING:
                status = transition(status, RunStatus.FAILED)
            self._store.save(
                RunState(
                    run_id,
                    status.value,
                    json.dumps(
                        {
                            "task_id": str(contract.task_id),
                            "plan_id": str(plan.plan_id),
                            "error": str(exc)[:500],
                        }
                    ),
                )
            )
            self._audit_event(
                "task_failed",
                contract.task_id,
                run_id=run_id,
                success=False,
                metadata={"error": str(exc)[:200]},
            )
            raise
