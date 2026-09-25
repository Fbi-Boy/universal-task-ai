from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

StepKind = Literal["analyze", "tool", "agent", "review", "finalize"]

class PlanStep(BaseModel):
    """One bounded action in an execution plan."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    step_id: str = Field(min_length=1, max_length=100)
    kind: StepKind
    objective: str = Field(min_length=1, max_length=5_000)
    depends_on: list[str] = Field(default_factory=list)
    required_tools: list[str] = Field(default_factory=list)
    approval_required: bool = False
    max_attempts: int = Field(default=1, ge=1, le=5)

class ExecutionPlan(BaseModel):
    """Validated plan passed to the orchestrator."""

    model_config = ConfigDict(extra="forbid")

    plan_id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    steps: list[PlanStep] = Field(min_length=1, max_length=100)
    max_turns: int = Field(default=10, ge=1, le=100)
    rationale: str = Field(default="", max_length=10_000)
