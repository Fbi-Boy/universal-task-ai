from backend.core.diagram_artifact_validator import DiagramArtifactValidator
from backend.core.programming_artifacts import ProgrammingArtifact

def test_uml_markers_pass():
    c = DiagramArtifactValidator().validate(
        ProgrammingArtifact.UML, "CLASS User RELATIONSHIP Order"
    )
    assert c.passed

def test_sequence_markers_required():
    c = DiagramArtifactValidator().validate(
        ProgrammingArtifact.SEQUENCE_DIAGRAM, "ACTOR User"
    )
    assert not c.passed
