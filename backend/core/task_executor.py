import hashlib
import json
from dataclasses import dataclass
from uuid import UUID, uuid4

from backend.core.audit import AuditEvent
from backend.core.audit_sink import AuditSink
from backend.core.approval import ApprovalMachine, ApprovalState
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
    ) -> None:
        self._store = store
        self._tool_boundary = tool_boundary
        self._audit = audit_sink
        self._approvals = ApprovalMachine()

    def _audit_event(
        self,
        event_type: str,
        task_id: UUID,
        *,
        run_id: str,
        tool_name: str | None = None,
        success: bool | None = None,
        metadata: dict | None = None,
        actor: str = "orchestrator",
    ) -> None:
        if self._audit is None:
            return
        self._audit.append(
            AuditEvent(
                event_type=event_type,
                task_id=task_id,
                actor=actor,
                tool_name=tool_name,
                success=success,
                metadata={"run_id": run_id, **(metadata or {})},
            )
        )

    @staticmethod
    def _arguments_hash(invocation: ToolInvocation) -> str:
        canonical = json.dumps(
            invocation.arguments,
            sort_keys=True,
            separators=(",", ":"),
            default=lambda value: repr(value),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def _save(self, run_id: str, status: RunStatus, payload: dict) -> None:
        self._store.save(RunState(run_id, status.value, json.dumps(payload, sort_keys=True)))

    def execute(
        self,
        contract: TaskContract,
        plan: ExecutionPlan,
        *,
        tool_invocations: tuple[ToolInvocation, ...] = (),
    ) -> ExecutionResult:
        run_id = str(uuid4())
        status = RunStatus.CREATED
        self._save(run_id, status, {"task_id": str(contract.task_id)})
        self._audit_event("task_started", contract.task_id, run_id=run_id)
        status = transition(status, RunStatus.RUNNING)
        self._save(run_id, status, {"task_id": str(contract.task_id), "plan_id": str(plan.plan_id)})
        try:
            has_tool_stage = any(step.kind == "tool" for step in plan.steps)
            has_agent_stage = any(step.kind == "agent" for step in plan.steps)

            if has_agent_stage:
                raise RuntimeError("agent execution requires a registered side-effect boundary")

            if has_tool_stage:
                if self._tool_boundary is None:
                    raise RuntimeError("tool execution requires a configured runtime tool boundary")
                if not tool_invocations:
                    raise RuntimeError("tool plan requires at least one explicit tool invocation")

                outputs: list[str] = []
                for invocation in tool_invocations:
                    invocation.validate_bounds()
                    try:
                        prepared_tool = self._tool_boundary.prepare(invocation.tool_name)
                    except (ToolBoundaryDenied, PermissionError, ValueError) as exc:
                        self._audit_event(
                            "tool_denied", contract.task_id, run_id=run_id,
                            tool_name=invocation.tool_name, success=False,
                            metadata={"reason": str(exc)[:200]},
                        )
                        raise

                    if prepared_tool.metadata.requires_approval:
                        if len(tool_invocations) != 1:
                            raise RuntimeError("approval-gated runs currently require exactly one tool invocation")
                        approval = self._approvals.request(
                            contract.task_id,
                            f"execute tool {invocation.tool_name}",
                        )
                        self._save(
                            run_id,
                            transition(status, RunStatus.WAITING_APPROVAL),
                            {
                                "task_id": str(contract.task_id),
                                "plan_id": str(plan.plan_id),
                                "plan": plan.model_dump(mode="json"),
                                "approval_id": str(approval.approval_id),
                                "approval_state": ApprovalState.PENDING.value,
                                "tool_name": invocation.tool_name,
                                "arguments_sha256": self._arguments_hash(invocation),
                                "approval_action": approval.action,
                                "pending_tool_index": len(outputs),
                            },
                        )
                        return ExecutionResult(
                            run_id,
                            RunStatus.WAITING_APPROVAL,
                            f"Execution is waiting for approval. approval_id={approval.approval_id}",
                            plan,
                            str(approval.approval_id),
                        )

                    self._audit_event(
                        "tool_authorized", contract.task_id, run_id=run_id,
                        tool_name=invocation.tool_name,
                    )
                    self._audit_event(
                        "tool_started", contract.task_id, run_id=run_id,
                        tool_name=invocation.tool_name,
                    )
                    try:
                        result = self._tool_boundary.execute_authorized(
                            prepared_tool, invocation.arguments
                        )
                    except (ToolBoundaryDenied, PermissionError, ValueError) as exc:
                        self._audit_event(
                            "tool_denied", contract.task_id, run_id=run_id,
                            tool_name=invocation.tool_name, success=False,
                            metadata={"reason": str(exc)[:200]},
                        )
                        raise
                    self._audit_event(
                        "tool_finished", contract.task_id, run_id=run_id,
                        tool_name=invocation.tool_name, success=result.success,
                    )
                    if not result.success:
                        raise RuntimeError(result.error or "tool execution failed")
                    outputs.append(str(result.output))

                status = transition(status, RunStatus.SUCCEEDED)
                output = "\\n".join(outputs)
                self._save(run_id, status, {
                    "task_id": str(contract.task_id), "plan_id": str(plan.plan_id), "output": output,
                })
                self._audit_event("task_finished", contract.task_id, run_id=run_id, success=True)
                return ExecutionResult(run_id, status, output, plan)

            if contract.approval_required:
                status = transition(status, RunStatus.WAITING_APPROVAL)
                self._save(run_id, status, {
                    "task_id": str(contract.task_id), "plan_id": str(plan.plan_id),
                    "reason": "execution boundary requires approval",
                })
                return ExecutionResult(run_id, status, "Execution is waiting for approval.", plan)

            status = transition(status, RunStatus.SUCCEEDED)
            output = (
                "Task contract validated and execution completed through the safe baseline runtime. "
                "No external tools or side effects were invoked."
            )
            self._save(run_id, status, {
                "task_id": str(contract.task_id), "plan_id": str(plan.plan_id), "output": output,
            })
            self._audit_event("task_finished", contract.task_id, run_id=run_id, success=True)
            return ExecutionResult(run_id, status, output, plan)
        except Exception as exc:
            if status == RunStatus.RUNNING:
                status = transition(status, RunStatus.FAILED)
            self._save(run_id, status, {
                "task_id": str(contract.task_id), "plan_id": str(plan.plan_id), "error": str(exc)[:500],
            })
            self._audit_event(
                "task_failed", contract.task_id, run_id=run_id, success=False,
                metadata={"error": str(exc)[:200]},
            )
            raise

    def resume_approved(
        self,
        run_id: str,
        approval_id: str,
        invocation: ToolInvocation,
        actor_id: str,
    ) -> ExecutionResult:
        """Consume one persisted approval and execute its exact pending invocation once."""
        if not actor_id.strip():
            raise ValueError("actor_id is required")
        state = self._store.get(run_id)
        if state is None:
            raise ValueError("run not found")
        if state.status != RunStatus.WAITING_APPROVAL.value:
            raise ValueError("run is not waiting for approval")

        payload = json.loads(state.payload)
        if payload.get("approval_id") != approval_id:
            raise ValueError("approval does not match pending run")
        if payload.get("approval_state") != ApprovalState.PENDING.value:
            raise ValueError("approval has already been consumed or rejected")
        invocation.validate_bounds()
        if payload.get("tool_name") != invocation.tool_name:
            raise ValueError("tool does not match pending approval")
        if payload.get("arguments_sha256") != self._arguments_hash(invocation):
            raise ValueError("tool arguments do not match pending approval")
        if self._tool_boundary is None:
            raise RuntimeError("tool execution requires a configured runtime tool boundary")

        task_id = UUID(payload["task_id"])
        plan = ExecutionPlan.model_validate(payload["plan"])
        running = transition(RunStatus.WAITING_APPROVAL, RunStatus.RUNNING)
        payload["approval_state"] = ApprovalState.APPROVED.value
        self._save(run_id, running, payload)

        try:
            tool = self._tool_boundary.authorize(invocation.tool_name, approved=True)
            self._audit_event(
                "tool_authorized", task_id, run_id=run_id, tool_name=invocation.tool_name,
                actor=actor_id,
            )
            self._audit_event(
                "tool_started", task_id, run_id=run_id, tool_name=invocation.tool_name,
                actor=actor_id,
            )
            result = self._tool_boundary.execute_authorized(tool, invocation.arguments)
            self._audit_event(
                "tool_finished", task_id, run_id=run_id, tool_name=invocation.tool_name,
                success=result.success, actor=actor_id,
            )
            if not result.success:
                raise RuntimeError(result.error or "tool execution failed")
            payload.update({
                "approval_state": ApprovalState.CONSUMED.value,
                "output": str(result.output),
            })
            succeeded = transition(running, RunStatus.SUCCEEDED)
            self._save(run_id, succeeded, payload)
            self._audit_event("task_finished", task_id, run_id=run_id, success=True, actor=actor_id)
            return ExecutionResult(run_id, succeeded, str(result.output), plan)
        except Exception as exc:
            failed = transition(running, RunStatus.FAILED)
            payload.update({"approval_state": ApprovalState.CONSUMED.value, "error": str(exc)[:500]})
            self._save(run_id, failed, payload)
            self._audit_event(
                "task_failed", task_id, run_id=run_id, success=False,
                metadata={"error": str(exc)[:200]}, actor=actor_id,
            )
            raise
