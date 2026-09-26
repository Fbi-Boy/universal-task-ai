from backend.core.notification_dispatch import NotificationRoute, SafeNotificationDispatcher
from backend.core.notification_events import NotificationEvent, NotificationKind

class Adapter:
    def __init__(self): self.events=[]
    def send(self,event): self.events.append(event)

def test_only_matching_route_receives_event():
    a,b=Adapter(),Adapter()
    d=SafeNotificationDispatcher([
        NotificationRoute(NotificationKind.RUN_COMPLETED,a),
        NotificationRoute(NotificationKind.APPROVAL_REQUIRED,b),
    ])
    e=NotificationEvent(NotificationKind.RUN_COMPLETED,"r","u","done")
    assert d.dispatch(e)==1 and a.events==[e] and b.events==[]

def test_missing_route_fails_closed():
    try:
        SafeNotificationDispatcher([]).dispatch(NotificationEvent(NotificationKind.RUN_FAILED,"r","u","x"))
        assert False
    except LookupError:
        assert True
