import json
import re
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from backend.core.analyzer import AmbiguityLevel, TaskAnalysis
from backend.core.agent_context import build_agent_messages
from backend.core.model_gateway import ModelGateway, ModelRequest
from backend.core.schemas import TaskContract

_MAX_REQUIREMENTS = 32
_MAX_REASON_LENGTH = 512
_CODE_FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.DOTALL)


class AnalysisGateway(Protocol):
    def generate(self, request: ModelRequest): ...


class ModelAnalysisDocument(BaseModel):
    """Strict, bounded JSON shape accepted from an untrusted model."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    normalized_goal: str = Field(min_length=1, max_length=20_000)
    requirements: list[str] = Field(default_factory=list, max_length=_MAX_REQUIREMENTS)
    ambiguity_level: AmbiguityLevel = "low"
    ambiguity_reasons: list[str] = Field(default_factory=list, max_length=16)
    assumptions: list[str] = Field(default_factory=list, max_length=16)
    needs_clarification: bool = False


class ModelTaskAnalyzer:
    """Use a model only to enrich understanding; execution remains deterministic."""

    def __init__(self, gateway: ModelGateway) -> None:
        self._gateway = gateway

    def analyze(self, task_text: str) -> TaskAnalysis:
        task_text = task_text.strip()
        if not task_text:
            raise ValueError("task_text must not be empty")

        # The model receives a bounded contract projection, never credentials or
        # runtime capability internals.
        contract = TaskContract(goal=task_text)
        messages = build_agent_messages(contract)
        messages.append(
            messages[-1].model_copy(
                update={
                    "role": "user",
                    "content": (
                        "Return JSON only with exactly these fields: "
                        "normalized_goal, requirements, ambiguity_level, "
                        "ambiguity_reasons, assumptions, needs_clarification. "
                        "Do not add permissions, tools, credentials, or executable instructions."
                    ),
                }
            )
        )
        response = self._gateway.generate(ModelRequest(messages=messages, max_output_tokens=1_500))
        document = self._parse_response(response.content)

        # Re-check model output with the same hard bounds used by the local schema.
        requirements = [item.strip() for item in document.requirements if item.strip()]
        reasons = [item[:_MAX_REASON_LENGTH] for item in document.ambiguity_reasons if item.strip()]
        assumptions = [item[:_MAX_REASON_LENGTH] for item in document.assumptions if item.strip()]
        return TaskAnalysis(
            normalized_goal=document.normalized_goal,
            requirements=requirements,
            ambiguity_level=document.ambiguity_level,
            ambiguity_reasons=reasons,
            assumptions=assumptions,
            needs_clarification=document.needs_clarification,
        )

    @staticmethod
    def _parse_response(content: str) -> ModelAnalysisDocument:
        candidate = content.strip()
        match = _CODE_FENCE.match(candidate)
        if match:
            candidate = match.group(1).strip()
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError as exc:
            raise ValueError("model analysis must be valid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("model analysis must be a JSON object")
        return ModelAnalysisDocument.model_validate(payload)
