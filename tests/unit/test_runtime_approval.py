from backend.core.runtime_approval import RuntimeApprovalService
from backend.core.approval_notifications import ApprovalNotificationMapper
from backend.core.approval_resume import ApprovalResumeRequest

class N:
    def dispatch(self,e): return 1
class R:
    def handle(self,r): return r.approved

def test_runtime_approval_keeps_resume_gateway_explicit():
    s=RuntimeApprovalService(ApprovalNotificationMapper(),N(),R())
    assert s.request("run","approval","user")==1
    assert s.resume(ApprovalResumeRequest("run","approval",True,"actor")) is True
