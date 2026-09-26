from backend.core.schedule_notifications import ScheduleNotificationMapper
from backend.core.scheduler_notifications import SchedulerNotificationFlow
from backend.core.notification_events import NotificationKind

class Notifier:
    def __init__(self): self.events=[]
    def dispatch(self,event): self.events.append(event); return 1

def test_completed_run_reaches_notification_pipeline():
    n=Notifier()
    SchedulerNotificationFlow(ScheduleNotificationMapper(),n).publish("run-1","user-1","completed","done")
    assert n.events[0].kind is NotificationKind.RUN_COMPLETED

def test_failed_run_reaches_notification_pipeline():
    n=Notifier()
    SchedulerNotificationFlow(ScheduleNotificationMapper(),n).publish("run-1","user-1","failed","failed")
    assert n.events[0].kind is NotificationKind.RUN_FAILED

def test_unknown_status_fails_closed():
    try:
        SchedulerNotificationFlow(ScheduleNotificationMapper(),Notifier()).publish("r","u","running","x")
        assert False
    except ValueError:
        assert True
