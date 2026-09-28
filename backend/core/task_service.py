from dataclasses import dataclass
from typing import Literal

from backend.core.approval_store import ApprovalStore
from backend.core.task_executor import ExecutionResult, TaskExecutor
from backend.core.intent_router import SafeTaskIntentRouter
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner
from backend.core.tool_invocation import ToolInvocation


@dataclass(frozen=True)
class TaskRunResult:
    intake: object
    execution: ExecutionResult
    routing_mode: Literal["safe_baseline", "explicit_tool", "auto_calculator", "auto_local_read"]
    routed_tools: tuple[str, ...]


class TaskService:
    """Application service connecting intake, planning, execution, and resume."""

    def __init__(
        self,
        intake: TaskIntakeService,
        planner: TaskPlanner,
        executor: TaskExecutor,
        intent_router: SafeTaskIntentRouter | None = None,
    ) -> None:
        self._intake = intake
        self._planner = planner
        self._executor = executor
        self._intent_router = intent_router or SafeTaskIntentRouter()

    @property
    def tool_catalog(self):
        """Return metadata for tools allowed by the runtime boundary."""
        return self._executor.tool_catalog

    @property
    def approval_store(self) -> ApprovalStore | None:
        """Expose the executor's approval store for API composition."""
        return self._executor.approval_store

    def readiness(self) -> dict[str, str]:
        """Probe durable runtime dependencies without executing user work."""
        return self._executor.readiness()

    def run(
        self,
        task_text: str,
        *,
        tool_invocations: tuple[ToolInvocation, ...] = (),
        approval_required: bool = False,
        auto_route_tools: bool = True,
    ) -> TaskRunResult:
        intake = self._intake.intake(task_text)
        routing_mode: Literal["safe_baseline", "explicit_tool", "auto_calculator"] = "safe_baseline"
        if tool_invocations:
            routing_mode = "explicit_tool"
        elif auto_route_tools:
            available_tool_names = {item.name for item in self.tool_catalog}
            suggested = self._intent_router.route(
                task_text,
                available_tools=available_tool_names,
            )
            if suggested is not None:
                tool_invocations = (suggested,)
                routing_mode = "auto_calculator" if suggested.tool_name == "calculator" else "auto_local_read"
        if len(tool_invocations) > 8:
            raise ValueError("at most 8 tool invocations are allowed per task")
        for invocation in tool_invocations:
            invocation.validate_bounds()

        contract = intake.contract.model_copy(
            update={
                "tools_allowed": list(dict.fromkeys(item.tool_name for item in tool_invocations)),
                "tools_required": list(dict.fromkeys(item.tool_name for item in tool_invocations)),
                "approval_required": approval_required,
            }
        )
        plan = self._planner.plan(contract)
        execution = self._executor.execute(
            contract,
            plan,
            tool_invocations=tool_invocations,
        )
        return TaskRunResult(
            intake=intake,
            execution=execution,
            routing_mode=routing_mode,
            routed_tools=tuple(dict.fromkeys(item.tool_name for item in tool_invocations)),
        )

    def resume_approved(
        self,
        *,
        run_id: str,
        approval_id: str,
        actor_id: str,
    ) -> ExecutionResult:
        return self._executor.resume_approved_from_run(
            run_id=run_id,
            approval_id=approval_id,
            actor_id=actor_id,
        )
