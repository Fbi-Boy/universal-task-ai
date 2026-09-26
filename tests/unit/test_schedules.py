from datetime import datetime, timedelta, timezone

import pytest

from backend.core.schedules import ScheduleDispatcher, ScheduledTask


def test_once_schedule_requires_timezone_aware_time() -> None:
    with pytest.raises(ValueError):
        ScheduledTask.once(user_id="u1", task="check campus", run_at=datetime.now())


def test_due_once_schedule_dispatches_normal_task() -> None:
    now = datetime.now(timezone.utc)
    schedule = ScheduledTask.once(user_id="u1", task="check campus attendance", run_at=now)
    dispatcher = ScheduleDispatcher()

    event = dispatcher.dispatch(schedule, now=now + timedelta(seconds=1))

    assert event.user_id == "u1"
    assert event.task == "check campus attendance"
    assert dispatcher.history() == (event,)


def test_future_schedule_is_not_dispatched() -> None:
    now = datetime.now(timezone.utc)
    schedule = ScheduledTask.once(user_id="u1", task="check campus", run_at=now + timedelta(hours=1))
    dispatcher = ScheduleDispatcher()

    with pytest.raises(ValueError):
        dispatcher.dispatch(schedule, now=now)


def test_interval_bounds_are_explicit() -> None:
    with pytest.raises(ValueError):
        ScheduledTask.interval(user_id="u1", task="check", interval_seconds=30)

    schedule = ScheduledTask.interval(user_id="u1", task="check", interval_seconds=300)
    assert schedule.interval_seconds == 300
