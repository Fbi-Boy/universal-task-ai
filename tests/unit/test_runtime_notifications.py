from backend.core.runtime_notifications import RuntimeNotificationService
from backend.core.notification_dispatch import NotificationRoute
from backend.core.notification_events import NotificationEvent,NotificationKind

class A:
    def __init__(self): self.events=[]
    def send(self,e): self.events.append(e)

def test_runtime_notification_service_uses_explicit_routes():
    a=A()
    service=RuntimeNotificationService([NotificationRoute(NotificationKind.RUN_COMPLETED,a)])
    event=NotificationEvent(NotificationKind.RUN_COMPLETED,"r","u","done")
    assert service.publish(event)==1 and a.events==[event]
