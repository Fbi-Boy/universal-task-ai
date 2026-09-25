from dataclasses import dataclass
from typing import Literal

from backend.core.schemas import TaskContract

RouteKind = Literal["direct", "tool", "agent", "clarification"]

@dataclass(frozen=True)
class RouteDecision:
    kind: RouteKind
    reason: str

def choose_route(task: TaskContract) -> RouteDecision:
    if task.approval_required and task.risk_level in {"high", "critical"}:
        return RouteDecision("clarification", "approval is required before execution")

    if task.tools_required:
        return RouteDecision("tool", "task explicitly requires one or more tools")

    if task.risk_level == "medium":
        return RouteDecision("agent", "medium-risk work requires controlled agent execution")

    return RouteDecision("direct", "task can be handled without external execution")
