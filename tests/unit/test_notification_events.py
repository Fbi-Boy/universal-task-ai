from backend.core.notification_events import NotificationEvent, NotificationKind, NotificationRouter

class Adapter:
    def __init__(self): self.events = []
    def send(self, event): self.events.append(event)

def test_router_dispatches_event_to_adapters():
    a, b = Adapter(), Adapter()
    e = NotificationEvent(NotificationKind.RUN_COMPLETED, "run-1", "u-1", "done")
    NotificationRouter([a, b]).dispatch(e)
    assert a.events == [e] and b.events == [e]

def test_router_bounds_message():
    try:
        NotificationRouter([]).dispatch(
            NotificationEvent(NotificationKind.RUN_FAILED, "r", "u", "x" * 4097)
        )
        assert False
    except ValueError:
        assert True
