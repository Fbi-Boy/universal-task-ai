from dataclasses import dataclass

from backend.core.planner import ExecutionPlan

@dataclass(frozen=True)
class PlanValidationResult:
    passed: bool
    errors: tuple[str, ...]

def validate_execution_plan(plan: ExecutionPlan) -> PlanValidationResult:
    errors: list[str] = []
    ids = [step.step_id for step in plan.steps]
    id_set = set(ids)

    if len(ids) != len(id_set):
        errors.append("plan step IDs must be unique")

    for step in plan.steps:
        missing = set(step.depends_on) - id_set
        if missing:
            errors.append(
                f"step {step.step_id} depends on unknown steps: "
                + ", ".join(sorted(missing))
            )
        if step.step_id in step.depends_on:
            errors.append(f"step {step.step_id} cannot depend on itself")

    if plan.max_turns < len(plan.steps):
        errors.append("max_turns must be at least the number of plan steps")

    # Detect dependency cycles with a small DFS so the orchestrator never
    # receives a plan that cannot make forward progress.
    graph = {step.step_id: set(step.depends_on) for step in plan.steps}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited or node not in graph:
            return
        if node in visiting:
            errors.append("plan dependency graph contains a cycle")
            return
        visiting.add(node)
        for dependency in graph[node]:
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)

    return PlanValidationResult(passed=not errors, errors=tuple(dict.fromkeys(errors)))
