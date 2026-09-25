from typing import Any, Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field, field_validator

RiskLevel = Literal["low", "medium", "high", "critical"]

class TaskContract(BaseModel):
    """Normalized specification passed from understanding into execution."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    task_id: UUID = Field(default_factory=uuid4)
    goal: str = Field(min_length=1, max_length=20_000)
    input: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    language: str | None = None
    output: str | None = None
    format: str | None = None
    style: str | None = None
    constraints: list[str] = Field(default_factory=list)
    deadline: str | None = None
    tools_allowed: list[str] = Field(default_factory=list)
    tools_required: list[str] = Field(default_factory=list)
    risk_level: RiskLevel = "low"
    approval_required: bool = False
    success_criteria: list[str] = Field(default_factory=list)
    validation_rules: list[str] = Field(default_factory=list)

    @field_validator("tools_allowed", "tools_required", "constraints", "success_criteria", "validation_rules")
    @classmethod
    def reject_blank_items(cls, values: list[str]) -> list[str]:
        if any(not item.strip() for item in values):
            raise ValueError("list items must not be blank")
        return values
