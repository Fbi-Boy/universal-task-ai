from backend.core.schedule_notifications import ScheduleNotificationMapper

class SchedulerNotificationFlow:
    """Maps a completed/failed scheduled run into the notification pipeline."""
    def __init__(self, mapper, notifier):
        self.mapper = mapper
        self.notifier = notifier

    def publish(self, run_id, user_id, status, message):
        event = self.mapper.to_event(__import__("backend.core.schedule_notifications", fromlist=["ScheduleNotification"]).ScheduleNotification(run_id,user_id,status,message))
        return self.notifier.dispatch(event)
