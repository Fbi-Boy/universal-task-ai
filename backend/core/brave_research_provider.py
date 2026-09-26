from backend.core.research_evidence import EvidenceBundle
from backend.core.research_provider import ResearchProviderRequest

class BraveResearchProvider:
    """Adapts the existing Brave provider contract to EvidenceBundle."""
    def __init__(self, brave_provider):
        self.brave_provider=brave_provider

    def search(self, request: ResearchProviderRequest) -> EvidenceBundle:
        if not request.query or len(request.query)>1000:
            raise ValueError("invalid query")
        if not 1<=request.limit<=20:
            raise ValueError("limit out of bounds")
        bundle=self.brave_provider.search(request.query,request.limit)
        if not isinstance(bundle,EvidenceBundle):
            raise TypeError("Brave provider must return EvidenceBundle")
        return bundle.validate()
