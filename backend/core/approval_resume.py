from dataclasses import dataclass

@dataclass(frozen=True)
class ApprovalResumeRequest:
    run_id: str
    approval_id: str
    approved: bool
    actor_id: str

class ApprovalResumeGateway:
    def __init__(self,resume):
        self.resume=resume
    def handle(self,request:ApprovalResumeRequest):
        if not request.run_id or not request.approval_id or not request.actor_id:
            raise ValueError("approval identity is required")
        return self.resume(request.run_id,request.approval_id,request.approved,request.actor_id)
