from dataclasses import dataclass
from backend.core.programming_artifacts import ProgrammingArtifact

@dataclass(frozen=True)
class DiagramCheck:
    artifact: ProgrammingArtifact
    passed: bool
    reason: str

class DiagramArtifactValidator:
    def validate(self, artifact, content):
        if artifact not in {
            ProgrammingArtifact.UML,
            ProgrammingArtifact.SEQUENCE_DIAGRAM,
        }:
            raise ValueError("unsupported diagram artifact")
        if not content or not content.strip():
            return DiagramCheck(artifact, False, "empty artifact")
        upper = content.upper()
        required = ("CLASS", "RELATIONSHIP") if artifact is ProgrammingArtifact.UML else ("ACTOR", "SEQUENCE")
        missing = [m for m in required if m not in upper]
        if missing:
            return DiagramCheck(artifact, False, "missing markers: " + ",".join(missing))
        return DiagramCheck(artifact, True, "basic structural markers present")
