from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict

class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool
    output: Any = None
    error: str | None = None

@dataclass(frozen=True)
class ToolMetadata:
    name: str
    description: str
    risk_level: str = "low"
    requires_network: bool = False
    requires_approval: bool = False

class Tool(ABC):
    metadata: ToolMetadata

    @abstractmethod
    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        raise NotImplementedError

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        name = tool.metadata.name
        if name in self._tools:
            raise ValueError(f"tool already registered: {name}")
        self._tools[name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {name}") from exc

    def metadata(self) -> tuple[ToolMetadata, ...]:
        return tuple(tool.metadata for tool in self._tools.values())
