from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from backend.core.tools import ToolResult


class ToolArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    tool_name: str = Field(min_length=1, max_length=100)
    arguments: dict[str, Any] = Field(default_factory=dict)


def validate_tool_result(result: ToolResult) -> ToolResult:
    if result.success and result.error is not None:
        raise ValueError("successful tool results must not contain an error")
    if not result.success and not result.error:
        raise ValueError("failed tool results must contain an error")
    return result
