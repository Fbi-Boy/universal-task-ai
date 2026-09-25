from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Callable


class FailureKind(StrEnum):
    VALIDATION = "validation"
    PERMISSION = "permission"
    TOOL = "tool"
    TIMEOUT = "timeout"
    TRANSIENT = "transient"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Failure:
    kind: FailureKind
    message: str
    retryable: bool


def classify_failure(exc: BaseException) -> Failure:
    name = type(exc).__name__.lower()
    if "permission" in name:
        return Failure(FailureKind.PERMISSION, str(exc), False)
    if "timeout" in name:
        return Failure(FailureKind.TIMEOUT, str(exc), True)
    if isinstance(exc, ValueError):
        return Failure(FailureKind.VALIDATION, str(exc), False)
    return Failure(FailureKind.UNKNOWN, str(exc), False)


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        if not 1 <= self.max_attempts <= 5:
            raise ValueError("max_attempts must be between 1 and 5")

    def run(self, operation: Callable[[], Any]) -> Any:
        last: BaseException | None = None
        for _ in range(self.max_attempts):
            try:
                return operation()
            except BaseException as exc:
                last = exc
                if not classify_failure(exc).retryable:
                    raise
        assert last is not None
        raise last
