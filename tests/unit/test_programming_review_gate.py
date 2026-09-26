from backend.core.programming_review_gate import ProgrammingReviewGate
class Check:
    def __init__(self,passed,reason): self.passed,self.reason=passed,reason
def test_gate_passes_when_all_checks_pass(): assert ProgrammingReviewGate().review([Check(True,"ok")]).passed
def test_gate_reports_failed_checks():
    d=ProgrammingReviewGate().review([Check(False,"missing key")])
    assert not d.passed and d.reasons==("missing key",)
