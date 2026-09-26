from dataclasses import dataclass
from backend.core.research_evidence import EvidenceBundle

@dataclass(frozen=True)
class ResearchProviderRequest:
    query: str
    limit: int = 5

class ResearchProvider:
    def __init__(self, search_provider):
        self.search_provider = search_provider

    def search(self, request: ResearchProviderRequest):
        if not request.query or len(request.query)>1000: raise ValueError("invalid query")
        if not 1<=request.limit<=20: raise ValueError("limit out of bounds")
        bundle=self.search_provider.search(request.query,request.limit)
        if not isinstance(bundle,EvidenceBundle): raise TypeError("provider must return EvidenceBundle")
        return bundle
