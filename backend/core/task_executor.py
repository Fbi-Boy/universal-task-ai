import json
from dataclasses import dataclass
from uuid import UUID, uuid4

from backend.core.approval_store import ApprovalStore
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
    approval_id: str | None = None


class TaskExecutor:
    """Execute safe stages and explicitly bounded registered tool invocations."""

    def __init__(
        self,
        store: SQLiteRunStateStore,
        tool_boundary: RuntimeToolBoundary | None = None,
        audit_sink: AuditSink | None = None,
        approval_store: ApprovalStore | None = None,
    ) -> None:
        self._store = store
        self._tool_boundary = tool_boundary
        self._audit = audit_sink
        self._approvals = approval_store

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

            if has_tool_stage:
                if self._tool_boundary is None:
                    raise RuntimeError("tool execution requires a configured side-effect boundary")
                if not tool_invocations:
                    raise RuntimeError("tool plan requires at least one explicit tool invocation")

                if contract.approval_required:
                    if self._approvals is None:
                        raise RuntimeError("approval-required tool execution requires a durable approval store")
                    request = self._approvals.create_execution(
                        contract.task_id,
                        run_id,
                        plan.plan_id,
                        tool_invocations,
                        action=f"execute {len(tool_invocations)} bounded tool invocation(s)",
                    )
                    status = transition(status, RunStatus.WAITING_APPROVAL)
                    self._store.save(
                        RunState(
                            run_id,
                            status.value,
                            json.dumps(
                                {
                                    "task_id": str(contract.task_id),
                                    "plan_id": str(plan.plan_id),
                                    "approval_id": str(request.request.approval_id),
                                    "reason": "explicit approval required before tool execution",
                                }
                            ),
                        )
                    )
                    self._audit_event(
                        "tool_denied",
                        contract.task_id,
                        run_id=run_id,
                        success=False,
                        metadata={
                            "reason": "approval_pending",
                            "approval_id": str(request.request.approval_id),
                        },
                    )
                    return ExecutionResult(
                        run_id,
                        status,
                        "Execution is waiting for approval.",
                        plan,
                        str(request.request.approval_id),
                    )

                return self._run_tools(
                    contract,
                    plan,
                    run_id=run_id,
                    status=status,
                    tool_invocations=tool_invocations,
                    approval_consumed=False,
                )

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

            return self._finish_success(
                contract,
                plan,
                run_id=run_id,
                output=(
                    "Task contract validated and execution completed through the safe baseline runtime. "
                    "No external tools or side effects were invoked."
                ),
            )
        except Exception as exc:
            self._fail(contract, plan, run_id, status, exc)
            raise

    def resume_approved(
        self,
        contract: TaskContract,
        plan: ExecutionPlan,
        *,
        run_id: str,
        approval_id: str,
        actor_id: str,
    ) -> ExecutionResult:
        """Consume one approved execution and resume it once.

        Approval consumption is atomic and happens before tool execution. This
        prevents duplicate resumes. If a process crashes after consumption,
        recovery must use the durable run state rather than re-consuming approval.
        """
        if not actor_id.strip():
            raise ValueError("actor_id must not be empty")
        if self._approvals is None:
            raise RuntimeError("approval resume requires a durable approval store")
        if self._tool_boundary is None:
            raise RuntimeError("approval resume requires a configured side-effect boundary")

        state = self._store.get(run_id)
        if state is None:
            raise KeyError("run not found")
        if state.status != RunStatus.WAITING_APPROVAL.value:
            raise ValueError("run is not waiting for approval")

        payload = json.loads(state.payload)
        if payload.get("task_id") != str(contract.task_id):
            raise ValueError("approval task does not match run")
        if payload.get("plan_id") != str(plan.plan_id):
            raise ValueError("approval plan does not match run")
        if payload.get("approval_id") != approval_id:
            raise ValueError("approval does not match waiting run")

        execution = self._approvals.consume_execution(UUID(approval_id))
        if execution.run_id != run_id or execution.request.task_id != contract.task_id:
            raise ValueError("approval execution does not match waiting run")
        if execution.plan_id != plan.plan_id:
            raise ValueError("approval execution does not match plan")

        status = transition(RunStatus.WAITING_APPROVAL, RunStatus.RUNNING)
        self._store.save(
            RunState(
                run_id,
                status.value,
                json.dumps(
                    {
                        "task_id": str(contract.task_id),
                        "plan_id": str(plan.plan_id),
                        "approval_id": approval_id,
                        "approved_by": actor_id[:128],
                    }
                ),
            )
        )
        try:
            return self._run_tools(
                contract,
                plan,
                run_id=run_id,
                status=status,
                tool_invocations=execution.invocations,
                approval_consumed=True,
            )
        except Exception as exc:
            self._fail(contract, plan, run_id, status, exc)
            raise

    def _run_tools(
        self,
        contract: TaskContract,
        plan: ExecutionPlan,
        *,
        run_id: str,
        status: RunStatus,
        tool_invocations: tuple[ToolInvocation, ...],
        approval_consumed: bool,
    ) -> ExecutionResult:
        outputs: list[str] = []
        for invocation in tool_invocations:
            invocation.validate_bounds()
            try:
                authorized_tool = self._tool_boundary.authorize(
                    invocation.tool_name,
                    approved=approval_consumed,
                )  # type: ignore[union-attr]
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
                result = self._tool_boundary.execute_authorized(authorized_tool, invocation.arguments)  # type: ignore[union-attr]
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

        return self._finish_success(
            contract,
            plan,
            run_id=run_id,
            output="\n".join(outputs),
        )

    def _finish_success(
        self,
        contract: TaskContract,
        plan: ExecutionPlan,
        *,
        run_id: str,
        output: str,
    ) -> ExecutionResult:
        status = RunStatus.RUNNING
        if self._store.get(run_id) and self._store.get(run_id).status == RunStatus.CREATED.value:
            status = transition(RunStatus.CREATED, RunStatus.RUNNING)
        status = transition(status, RunStatus.SUCCEEDED)
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

    def _fail(
        self,
        contract: TaskContract,
        plan: ExecutionPlan,
        run_id: str,
        status: RunStatus,
        exc: Exception,
    ) -> None:
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
