from backend.core.artifact_validation import ArtifactValidator
from backend.core.programming_artifacts import ProgrammingArtifact


def test_validator_rejects_empty_artifact():
    result = ArtifactValidator().validate(ProgrammingArtifact.ERD, "")
    assert not result.passed


def test_validator_accepts_nonempty_code():
    result = ArtifactValidator().validate(ProgrammingArtifact.CODE, "print(1)")
    assert result.passed


def test_flowchart_requires_valid_start_and_end():
    result = ArtifactValidator().validate(
        ProgrammingArtifact.FLOWCHART,
        "START -> Validate input -> END",
    )
    assert result.passed


def test_flowchart_rejects_disconnected_structure():
    result = ArtifactValidator().validate(
        ProgrammingArtifact.FLOWCHART,
        "START -> Validate input",
    )
    assert not result.passed
    assert "flow does not end with END" in result.issues


def test_erd_requires_primary_and_foreign_keys():
    result = ArtifactValidator().validate(
        ProgrammingArtifact.ERD,
        "TABLE users\n id PK\nTABLE orders\n user_id FK",
    )
    assert result.passed


def test_erd_rejects_duplicate_entities():
    result = ArtifactValidator().validate(
        ProgrammingArtifact.ERD,
        "TABLE users\n id PK\nTABLE users\n user_id FK",
    )
    assert not result.passed
    assert "duplicate entity/table names" in result.issues


def test_sequence_diagram_requires_structural_markers():
    result = ArtifactValidator().validate(
        ProgrammingArtifact.SEQUENCE_DIAGRAM,
        "ACTOR User\nSEQUENCE User -> API",
    )
    assert result.passed


def test_artifact_size_is_bounded():
    result = ArtifactValidator().validate(
        ProgrammingArtifact.CODE,
        "x" * (256 * 1024 + 1),
    )
    assert not result.passed
    assert "artifact exceeds 256 KiB" in result.issues
