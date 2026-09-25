from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from backend.core.requirement_extractor import extract_requirements

AmbiguityLevel = Literal["low", "medium", "high"]

_HIGH_AMBIGUITY = ("terserah", "whatever", "something", "bebas")
_MEDIUM_AMBIGUITY = ("sesuai kebutuhan", "yang bagus", "best", "bagus")

class TaskAnalysis(BaseModel):
    """Deterministic analysis envelope produced before planning."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    normalized_goal: str = Field(min_length=1, max_length=20_000)
    requirements: list[str] = Field(default_factory=list)
    ambiguity_level: AmbiguityLevel = "low"
    ambiguity_reasons: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    needs_clarification: bool = False

    @classmethod
    def from_task_text(cls, task_text: str) -> "TaskAnalysis":
        text = task_text.strip()
        if not text:
            raise ValueError("task_text must not be empty")

        lowered = text.lower()
        high_matches = [marker for marker in _HIGH_AMBIGUITY if marker in lowered]
        medium_matches = [marker for marker in _MEDIUM_AMBIGUITY if marker in lowered]

        if high_matches:
            level: AmbiguityLevel = "high"
        elif medium_matches:
            level = "medium"
        else:
            level = "low"

        reasons = [
            f"underspecified language: {marker}"
            for marker in [*high_matches, *medium_matches]
        ]
        requirements = extract_requirements(text)

        return cls(
            normalized_goal=text,
            requirements=[item.description for item in requirements.items],
            ambiguity_level=level,
            ambiguity_reasons=list(dict.fromkeys(reasons)),
            needs_clarification=level == "high",
        )
