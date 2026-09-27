from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict


class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    output: Any = None
    error: str | None = None

    def validate_bounds(self) -> None:
        """Reject unbounded tool output before it reaches the runtime pipeline."""
        if self.error is not None and len(self.error) > 2_000:
            raise ValueError("tool error exceeds 2000 characters")
        if _nested_size(self.output) > 512:
            raise ValueError("tool output exceeds the maximum nested value count")


def _nested_size(value: Any, *, depth: int = 0) -> int:
    if depth > 8:
        raise ValueError("tool output exceeds maximum nesting depth")
    if isinstance(value, Mapping):
        if len(value) > 128:
            raise ValueError("tool output mapping exceeds 128 entries")
        return 1 + sum(
            _nested_size(k, depth=depth + 1) + _nested_size(v, depth=depth + 1)
            for k, v in value.items()
        )
    if isinstance(value, (list, tuple, set, frozenset)):
        if len(value) > 128:
            raise ValueError("tool output collection exceeds 128 entries")
        return 1 + sum(_nested_size(item, depth=depth + 1) for item in value)
    if isinstance(value, (str, bytes)) and len(value) > 64 * 1024:
        raise ValueError("tool output scalar exceeds 64 KiB")
    return 1


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
