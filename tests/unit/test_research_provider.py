from backend.core.research_provider import ResearchProvider,ResearchProviderRequest
from backend.core.research_evidence import Evidence,EvidenceBundle
class Provider:
    def search(self,q,limit): return EvidenceBundle(q,(Evidence("src","title","https://example.com","text"),))
def test_provider_returns_evidence():
    b=ResearchProvider(Provider()).search(ResearchProviderRequest("q",1))
    assert b.items[0].source=="src"
