from uuid import uuid4

import pytest

from backend.core.events import ExecutionEventBus


def test_event_bus_sequences_and_filters() -> None:
    bus = ExecutionEventBus(max_events_per_run=2)
    run_id = uuid4()
    bus.publish(run_id, "started", "one")
    second = bus.publish(run_id, "finished", "two")
    bus.publish(run_id, "extra", "three")
    events = bus.since(run_id, after=second.sequence)
    assert [event.kind for event in events] == ["extra"]


def test_event_bus_is_bounded_and_validates_input() -> None:
    bus = ExecutionEventBus(max_events_per_run=1)
    run_id = uuid4()
    bus.publish(run_id, "a")
    bus.publish(run_id, "b")
    assert len(bus.since(run_id)) == 1
    with pytest.raises(ValueError):
        bus.since(run_id, limit=101)
