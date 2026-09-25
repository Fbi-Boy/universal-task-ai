from dataclasses import dataclass

@dataclass(frozen=True)
class ExecutionBudget:
    max_turns: int = 10
    max_tool_calls: int = 10
    max_wall_time_seconds: int = 300

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not 1 <= self.max_turns <= 100:
            errors.append("max_turns must be between 1 and 100")
        if not 0 <= self.max_tool_calls <= 100:
            errors.append("max_tool_calls must be between 0 and 100")
        if not 1 <= self.max_wall_time_seconds <= 3600:
            errors.append("max_wall_time_seconds must be between 1 and 3600")
        return tuple(errors)

class BudgetExceeded(RuntimeError):
    pass

class BudgetTracker:
    def __init__(self, budget: ExecutionBudget) -> None:
        errors = budget.validate()
        if errors:
            raise ValueError("; ".join(errors))
        self.budget = budget
        self.turns = 0
        self.tool_calls = 0

    def consume_turn(self) -> None:
        if self.turns >= self.budget.max_turns:
            raise BudgetExceeded("maximum execution turns exceeded")
        self.turns += 1

    def consume_tool_call(self) -> None:
        if self.tool_calls >= self.budget.max_tool_calls:
            raise BudgetExceeded("maximum tool calls exceeded")
        self.tool_calls += 1
