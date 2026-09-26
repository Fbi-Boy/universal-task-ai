from dataclasses import dataclass
from backend.core.research_evidence import EvidenceBundle

@dataclass(frozen=True)
class ResearchResult:
    query: str
    evidence: EvidenceBundle

class ResearchOrchestrator:
    def __init__(self, searcher):
        self.searcher = searcher

    def run(self, query: str, limit=5):
        if not query or len(query) > 1000:
            raise ValueError("invalid query")
        if not 1 <= limit <= 20:
            raise ValueError("limit out of bounds")
        bundle = self.searcher.search(query, limit)
        if not isinstance(bundle, EvidenceBundle):
            raise TypeError("searcher must return EvidenceBundle")
        return ResearchResult(query, bundle)
