from backend.core.research_evidence import Evidence, EvidenceBundle
from backend.core.research_orchestration import ResearchOrchestrator

class Searcher:
    def search(self, query, limit):
        return EvidenceBundle(query, (Evidence("source", "title", "https://example.com", "excerpt"),))

def test_research_returns_evidence_bundle():
    result = ResearchOrchestrator(Searcher()).run("python", 1)
    assert result.evidence.items[0].url.startswith("https://")

def test_query_and_limit_are_bounded():
    try:
        ResearchOrchestrator(Searcher()).run("", 1)
        assert False
    except ValueError:
        assert True
