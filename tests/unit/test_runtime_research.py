from backend.core.runtime_research import RuntimeResearchService
from backend.core.research_provider import ResearchProviderRequest
from backend.core.research_evidence import Evidence,EvidenceBundle

class P:
    def search(self,q,limit):
        return EvidenceBundle(q,(Evidence("brave","t","https://example.com","x"),))

def test_runtime_research_returns_evidence():
    r=RuntimeResearchService(P()).search(ResearchProviderRequest("q",1))
    assert r.items[0].source=="brave"
