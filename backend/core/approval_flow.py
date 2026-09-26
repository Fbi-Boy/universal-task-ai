class ApprovalNotificationFlow:
    """Connects approval-required events with an explicit notifier and resume gateway."""
    def __init__(self, mapper, notifier, resume_gateway):
        self.mapper=mapper
        self.notifier=notifier
        self.resume_gateway=resume_gateway

    def request(self, run_id, approval_id, user_id):
        event=self.mapper.to_event(__import__("backend.core.approval_notifications", fromlist=["ApprovalNotification"]).ApprovalNotification(run_id,approval_id,user_id))
        return self.notifier.dispatch(event)

    def resume(self, request):
        return self.resume_gateway.handle(request)
