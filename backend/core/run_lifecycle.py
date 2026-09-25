from enum import StrEnum


class RunStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


_ALLOWED: dict[RunStatus, frozenset[RunStatus]] = {
    RunStatus.CREATED: frozenset({RunStatus.RUNNING, RunStatus.CANCELLED}),
    RunStatus.RUNNING: frozenset({RunStatus.WAITING_APPROVAL, RunStatus.SUCCEEDED, RunStatus.FAILED, RunStatus.CANCELLED}),
    RunStatus.WAITING_APPROVAL: frozenset({RunStatus.RUNNING, RunStatus.CANCELLED}),
    RunStatus.SUCCEEDED: frozenset(),
    RunStatus.FAILED: frozenset(),
    RunStatus.CANCELLED: frozenset(),
}


def can_transition(current: RunStatus, target: RunStatus) -> bool:
    return target in _ALLOWED[current]


def transition(current: RunStatus, target: RunStatus) -> RunStatus:
    if not can_transition(current, target):
        raise ValueError(f"invalid run transition: {current} -> {target}")
    return target
