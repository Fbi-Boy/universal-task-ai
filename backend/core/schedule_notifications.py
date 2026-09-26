from dataclasses import dataclass
from backend.core.notification_events import NotificationEvent, NotificationKind

@dataclass(frozen=True)
class ScheduleNotification:
    run_id: str
    user_id: str
    status: str
    message: str

class ScheduleNotificationMapper:
    def to_event(self, item: ScheduleNotification):
        if item.status == "completed":
            kind = NotificationKind.RUN_COMPLETED
        elif item.status == "failed":
            kind = NotificationKind.RUN_FAILED
        else:
            raise ValueError("unsupported schedule status")
        return NotificationEvent(kind, item.run_id, item.user_id, item.message)
