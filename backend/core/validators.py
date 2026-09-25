from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    message: str = ""


def validate_required_fields(value: dict[str, Any], fields: Iterable[str]) -> list[Check]:
    return [Check(field, field in value, f"missing required field: {field}") for field in fields]


def validate_output(value: Any, validators: Iterable[Callable[[Any], bool]]) -> list[Check]:
    checks: list[Check] = []
    for index, validator in enumerate(validators, start=1):
        try:
            passed = bool(validator(value))
        except Exception:
            passed = False
        checks.append(Check(f"validator_{index}", passed, "" if passed else "output validation failed"))
    return checks


def all_passed(checks: Iterable[Check]) -> bool:
    return all(check.passed for check in checks)
