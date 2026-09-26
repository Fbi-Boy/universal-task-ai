from dataclasses import dataclass
from backend.core.programming_artifacts import ProgrammingArtifact

@dataclass(frozen=True)
class ArtifactCheck:
    artifact: ProgrammingArtifact
    passed: bool
    issues: tuple[str,...]=()

class ArtifactValidator:
    def validate(self,artifact:ProgrammingArtifact,content:str)->ArtifactCheck:
        if not content.strip(): return ArtifactCheck(artifact,False,("artifact is empty",))
        return ArtifactCheck(artifact,True,())
