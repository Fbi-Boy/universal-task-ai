from backend.core.approval_flow import ApprovalNotificationFlow

class RuntimeApprovalService:
    def __init__(self, mapper, notifier, resume_gateway):
        self.flow=ApprovalNotificationFlow(mapper,notifier,resume_gateway)

    def request(self, run_id, approval_id, user_id):
        return self.flow.request(run_id,approval_id,user_id)

    def resume(self, request):
        return self.flow.resume(request)
