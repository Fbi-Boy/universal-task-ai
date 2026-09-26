from backend.core.approval_notifications import ApprovalNotification,ApprovalNotificationMapper
from backend.core.notification_events import NotificationKind
def test_approval_event_contains_reference():
    e=ApprovalNotificationMapper().to_event(ApprovalNotification("r","a","u"))
    assert e.kind is NotificationKind.APPROVAL_REQUIRED and "approval=a" in e.message
