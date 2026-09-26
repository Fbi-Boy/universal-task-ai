from backend.core.artifact_validation import ArtifactValidator
from backend.core.programming_artifacts import ProgrammingArtifact

def test_validator_rejects_empty_artifact():
    r=ArtifactValidator().validate(ProgrammingArtifact.ERD,"")
    assert not r.passed

def test_validator_accepts_nonempty_artifact():
    r=ArtifactValidator().validate(ProgrammingArtifact.FLOWCHART,"A -> B")
    assert r.passed
