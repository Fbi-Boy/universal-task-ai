from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

RequirementSource = Literal["explicit", "inferred"]
RequirementPriority = Literal["must", "should", "nice_to_have"]

class Requirement(BaseModel):
    """A normalized requirement extracted from a user's task."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    key: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=5_000)
    source: RequirementSource
    priority: RequirementPriority = "must"

class RequirementSet(BaseModel):
    """Requirements that downstream planning must preserve."""

    model_config = ConfigDict(extra="forbid")

    items: list[Requirement] = Field(default_factory=list)
