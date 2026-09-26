from backend.core.approval_resume import ApprovalResumeGateway,ApprovalResumeRequest

def test_approval_resume_preserves_actor():
    seen=[]
    ApprovalResumeGateway(lambda *x: seen.append(x)).handle(ApprovalResumeRequest("r","a",True,"u"))
    assert seen==[("r","a",True,"u")]
