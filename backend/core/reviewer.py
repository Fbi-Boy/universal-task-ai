from dataclasses import dataclass
from typing import Any, Callable, Iterable

from backend.core.validators import Check, validate_output


@dataclass(frozen=True)
class ReviewResult:
    passed: bool
    checks: tuple[Check, ...]

    @property
    def failures(self) -> tuple[Check, ...]:
        return tuple(check for check in self.checks if not check.passed)


class Reviewer:
    def review(
        self,
        output: Any,
        validators: Iterable[Callable[[Any], bool]] = (),
    ) -> ReviewResult:
        checks = tuple(validate_output(output, validators))
        return ReviewResult(passed=all(check.passed for check in checks), checks=checks)
