import pytest
from backend.core.research_evidence import Evidence,EvidenceBundle

def test_evidence_bundle_requires_https_sources():
    with pytest.raises(ValueError): EvidenceBundle("q",(Evidence("web","t","http://x","e"),)).validate()
