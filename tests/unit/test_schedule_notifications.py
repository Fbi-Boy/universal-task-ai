from backend.core.schedule_notifications import ScheduleNotification, ScheduleNotificationMapper
from backend.core.notification_events import NotificationKind

def test_completed_schedule_maps_to_completion_event():
    e = ScheduleNotificationMapper().to_event(
        ScheduleNotification("r1","u1","completed","done")
    )
    assert e.kind is NotificationKind.RUN_COMPLETED

def test_unknown_status_rejected():
    try:
        ScheduleNotificationMapper().to_event(ScheduleNotification("r","u","queued","x"))
        assert False
    except ValueError:
        assert True
