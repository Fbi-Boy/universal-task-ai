from dataclasses import dataclass

from backend.core.diagram_artifact_validator import DiagramArtifactValidator
from backend.core.erd_structural_validator import ERDStructuralValidator
from backend.core.erd_validator import ERDValidator
from backend.core.flowchart_structural_validator import FlowchartStructuralValidator
from backend.core.flowchart_validator import FlowchartValidator
from backend.core.programming_artifacts import ProgrammingArtifact


_MAX_CONTENT_BYTES = 256 * 1024


@dataclass(frozen=True)
class ArtifactCheck:
    artifact: ProgrammingArtifact
    passed: bool
    issues: tuple[str, ...] = ()


class ArtifactValidator:
    """Dispatch artifact-specific validation before programming results are accepted."""

    def __init__(self) -> None:
        self._flowchart = FlowchartValidator()
        self._flowchart_structure = FlowchartStructuralValidator()
        self._erd = ERDValidator()
        self._erd_structure = ERDStructuralValidator()
        self._diagram = DiagramArtifactValidator()

    def validate(self, artifact: ProgrammingArtifact, content: str) -> ArtifactCheck:
        if not isinstance(content, str):
            return ArtifactCheck(artifact, False, ("artifact content must be text",))
        if not content.strip():
            return ArtifactCheck(artifact, False, ("artifact is empty",))
        if len(content.encode("utf-8")) > _MAX_CONTENT_BYTES:
            return ArtifactCheck(artifact, False, ("artifact exceeds 256 KiB",))

        issues: list[str] = []
        if artifact is ProgrammingArtifact.FLOWCHART:
            basic = self._flowchart.validate(content)
            structural = self._flowchart_structure.validate(content)
            issues.extend(basic.issues)
            issues.extend(structural.issues)
        elif artifact is ProgrammingArtifact.ERD:
            basic = self._erd.validate(content)
            structural = self._erd_structure.validate(content)
            issues.extend(basic.issues)
            issues.extend(structural.issues)
        elif artifact in {
            ProgrammingArtifact.UML,
            ProgrammingArtifact.SEQUENCE_DIAGRAM,
        }:
            check = self._diagram.validate(artifact, content)
            if not check.passed:
                issues.append(check.reason)

        return ArtifactCheck(artifact, not issues, tuple(dict.fromkeys(issues)))
