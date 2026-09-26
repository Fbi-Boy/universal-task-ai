from dataclasses import dataclass
from datetime import datetime, timezone
from backend.core.schedule_store import ScheduleStore

@dataclass(frozen=True)
class ScheduledDispatch:
    schedule_id: str
    task_payload: str

class SchedulerWorker:
    """Claims due schedules and hands them to the normal task dispatcher."""
    def __init__(self, store: ScheduleStore, dispatcher):
        self.store=store
        self.dispatcher=dispatcher

    def poll_once(self, now: datetime) -> list[ScheduledDispatch]:
        now=now.astimezone(timezone.utc)
        dispatched=[]
        for record in self.store.due(now):
            if not self.store.claim(record.schedule_id,now):
                continue
            try:
                self.dispatcher.dispatch(record.task_payload)
                dispatched.append(ScheduledDispatch(record.schedule_id,record.task_payload))
            except Exception:
                self.store.complete_claim(record.schedule_id)
                raise
        return dispatched
