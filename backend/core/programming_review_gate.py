from dataclasses import dataclass
@dataclass(frozen=True)
class ReviewDecision:
    passed: bool
    reasons: tuple[str,...]
class ProgrammingReviewGate:
    def review(self,checks):
        failed=tuple(getattr(c,"reason","validation failed") for c in checks if not getattr(c,"passed",False))
        return ReviewDecision(not failed,failed)
