from backend.core.approval_flow import ApprovalNotificationFlow
from backend.core.approval_notifications import ApprovalNotificationMapper
from backend.core.approval_resume import ApprovalResumeRequest

class Notifier:
    def __init__(self): self.events=[]
    def dispatch(self,event): self.events.append(event); return 1

class Resume:
    def __init__(self): self.calls=[]
    def handle(self,request): self.calls.append(request); return "accepted"

def test_request_and_resume_are_separate_boundaries():
    n,r=Notifier(),Resume()
    flow=ApprovalNotificationFlow(ApprovalNotificationMapper(),n,r)
    assert flow.request("run","approval","user")==1
    req=ApprovalResumeRequest("run","approval",True,"actor")
    assert flow.resume(req)=="accepted"
    assert r.calls==[req]
