from backend.core.brave_research_provider import BraveResearchProvider
from backend.core.research_provider import ResearchProviderRequest
from backend.core.research_evidence import Evidence,EvidenceBundle

class Brave:
    def search(self,q,limit):
        return EvidenceBundle(q,(Evidence("brave","result","https://example.com","excerpt"),))

def test_brave_provider_returns_validated_evidence():
    result=BraveResearchProvider(Brave()).search(ResearchProviderRequest("query",1))
    assert result.items[0].source=="brave"

def test_invalid_provider_output_rejected():
    class Bad:
        def search(self,q,limit): return "not evidence"
    try:
        BraveResearchProvider(Bad()).search(ResearchProviderRequest("q",1))
        assert False
    except TypeError:
        assert True
