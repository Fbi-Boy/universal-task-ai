from dataclasses import dataclass
from enum import Enum

class NotificationKind(str, Enum):
    RUN_COMPLETED = "run.completed"
    RUN_FAILED = "run.failed"
    APPROVAL_REQUIRED = "approval.required"

@dataclass(frozen=True)
class NotificationEvent:
    kind: NotificationKind
    run_id: str
    user_id: str
    message: str

class NotificationRouter:
    def __init__(self, adapters):
        self.adapters = tuple(adapters)

    def dispatch(self, event: NotificationEvent):
        if not event.run_id or not event.user_id:
            raise ValueError("run_id and user_id are required")
        if len(event.message) > 4096:
            raise ValueError("message too large")
        for adapter in self.adapters:
            adapter.send(event)
