from backend.core.planner import ExecutionPlan, PlanStep
from backend.core.schemas import TaskContract

class TaskPlanner:
    """Builds a bounded, side-effect-free plan from a task contract."""

    def plan(self, contract: TaskContract) -> ExecutionPlan:
        steps = [
            PlanStep(step_id="analyze", kind="analyze", objective="Validate the normalized task contract before execution."),
        ]
        if contract.tools_required:
            steps.append(PlanStep(
                step_id="tools", kind="tool",
                objective="Execute explicitly required tools through the registered tool boundary.",
                depends_on=["analyze"], required_tools=list(contract.tools_required),
                approval_required=contract.approval_required,
            ))
            final_dependency = "tools"
        else:
            final_dependency = "analyze"
        steps.append(PlanStep(
            step_id="finalize", kind="finalize",
            objective="Produce a bounded execution result after all prior steps pass.",
            depends_on=[final_dependency],
        ))
        return ExecutionPlan(task_id=contract.task_id, steps=steps, max_turns=min(10, max(1, len(steps) * 2)),
                             rationale="Deterministic baseline plan; external side effects require explicit tool and approval boundaries.")
