from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class ScheduleKind(StrEnum):
    ONCE = "once"
    INTERVAL = "interval"


@dataclass(frozen=True)
class ScheduledTask:
    id: UUID
    user_id: str
    task: str
    kind: ScheduleKind
    run_at: datetime | None = None
    interval_seconds: int | None = None
    enabled: bool = True

    @classmethod
    def once(cls, *, user_id: str, task: str, run_at: datetime) -> "ScheduledTask":
        if not user_id or not task.strip():
            raise ValueError("user_id and task are required")
        if run_at.tzinfo is None:
            raise ValueError("run_at must be timezone-aware")
        return cls(uuid4(), user_id, task.strip(), ScheduleKind.ONCE, run_at=run_at)

    @classmethod
    def interval(cls, *, user_id: str, task: str, interval_seconds: int) -> "ScheduledTask":
        if not user_id or not task.strip():
            raise ValueError("user_id and task are required")
        if not 60 <= interval_seconds <= 31_536_000:
            raise ValueError("interval_seconds must be between 60 and 31536000")
        return cls(uuid4(), user_id, task.strip(), ScheduleKind.INTERVAL, interval_seconds=interval_seconds)

    def due(self, now: datetime) -> bool:
        if not self.enabled or now.tzinfo is None:
            return False
        if self.kind is ScheduleKind.ONCE:
            return self.run_at is not None and now >= self.run_at
        raise ValueError("interval schedules require a persisted last-run timestamp")


@dataclass(frozen=True)
class ScheduleDispatch:
    schedule_id: UUID
    user_id: str
    task: str
    requested_at: datetime


class ScheduleDispatcher:
    """Boundary between triggers and the normal task execution pipeline.

    Schedules never execute tools directly. They only enqueue a normal task,
    preserving the same permissions, approvals, review, audit, and retry rules
    as an interactive request.
    """

    def __init__(self) -> None:
        self._dispatches: list[ScheduleDispatch] = []

    def dispatch(self, schedule: ScheduledTask, *, now: datetime) -> ScheduleDispatch:
        if not schedule.due(now):
            raise ValueError("schedule is not due")
        event = ScheduleDispatch(schedule.id, schedule.user_id, schedule.task, now)
        self._dispatches.append(event)
        return event

    def history(self) -> tuple[ScheduleDispatch, ...]:
        return tuple(self._dispatches)
