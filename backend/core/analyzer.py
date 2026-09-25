from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

AmbiguityLevel = Literal["low", "medium", "high"]

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
        clarification_markers = (
            "terserah",
            "bebas",
            "whatever",
            "something",
            "sesuai kebutuhan",
            "yang bagus",
            "best",
        )
        reasons = [
            "task contains underspecified preference language"
            for marker in clarification_markers
            if marker in lowered
        ]

        level: AmbiguityLevel = "medium" if reasons else "low"
        return cls(
            normalized_goal=text,
            requirements=[text],
            ambiguity_level=level,
            ambiguity_reasons=list(dict.fromkeys(reasons)),
            needs_clarification=level == "high",
        )
