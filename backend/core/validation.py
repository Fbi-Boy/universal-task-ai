from dataclasses import dataclass
from typing import Any

from backend.core.schemas import TaskContract

@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    errors: tuple[str, ...]

def validate_task_contract(task: TaskContract) -> ValidationResult:
    errors: list[str] = []

    if not task.goal.strip():
        errors.append("goal must not be empty")

    if task.approval_required is False and task.risk_level in {"high", "critical"}:
        errors.append("high/critical risk tasks require approval")

    required = set(task.tools_required)
    allowed = set(task.tools_allowed)
    missing = required - allowed
    if missing:
        errors.append("required tools must be present in tools_allowed: " + ", ".join(sorted(missing)))

    return ValidationResult(passed=not errors, errors=tuple(errors))

def validate_output_schema(output: Any) -> ValidationResult:
    if output is None:
        return ValidationResult(False, ("output must not be None",))
    return ValidationResult(True, ())
