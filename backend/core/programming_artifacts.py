"""Programming-focused task and artifact contracts."""
from dataclasses import dataclass, field
from enum import Enum


class ProgrammingArtifact(str, Enum):
    CODE = "code"
    FLOWCHART = "flowchart"
    ERD = "erd"
    SEQUENCE_DIAGRAM = "sequence_diagram"
    UML = "uml"
    TEST_PLAN = "test_plan"
    TECHNICAL_DOCUMENT = "technical_document"
    SPREADSHEET = "spreadsheet"


@dataclass(frozen=True)
class ReferenceRequest:
    query: str
    sources: tuple[str, ...] = ("github", "web")
    max_sources: int = 5

    def __post_init__(self) -> None:
        if not self.query.strip():
            raise ValueError("reference query is required")
        if not self.sources:
            raise ValueError("at least one reference source is required")
        if self.max_sources < 1 or self.max_sources > 20:
            raise ValueError("max_sources must be between 1 and 20")


@dataclass(frozen=True)
class ProgrammingTask:
    goal: str
    artifacts: tuple[ProgrammingArtifact, ...] = field(default_factory=tuple)
    references: tuple[ReferenceRequest, ...] = field(default_factory=tuple)
    target_url: str | None = None

    def __post_init__(self) -> None:
        if not self.goal.strip():
            raise ValueError("programming task goal is required")
        if not self.artifacts:
            raise ValueError("at least one programming artifact is required")

    @property
    def needs_browser(self) -> bool:
        return self.target_url is not None

    @property
    def needs_research(self) -> bool:
        return bool(self.references)
