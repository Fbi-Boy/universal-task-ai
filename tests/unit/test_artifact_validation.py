from backend.core.artifact_validation import ArtifactValidator
from backend.core.programming_artifacts import ProgrammingArtifact


def test_validator_rejects_empty_artifact():
    result = ArtifactValidator().validate(ProgrammingArtifact.ERD, "")
    assert not result.passed


def test_validator_accepts_nonempty_artifact():
    result = ArtifactValidator().validate(
        ProgrammingArtifact.FLOWCHART,
        "START -> A -> END",
    )
    assert result.passed
