from dataclasses import dataclass
from backend.core.notification_events import NotificationEvent, NotificationKind
@dataclass(frozen=True)
class ApprovalNotification:
    run_id:str
    approval_id:str
    user_id:str
class ApprovalNotificationMapper:
    def to_event(self,item:ApprovalNotification):
        if not item.run_id or not item.approval_id or not item.user_id: raise ValueError("approval identifiers are required")
        return NotificationEvent(NotificationKind.APPROVAL_REQUIRED,item.run_id,item.user_id,f"Approval required for run {item.run_id}; approval={item.approval_id}")
