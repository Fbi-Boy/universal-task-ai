from abc import ABC, abstractmethod
from typing import Any, Mapping, Protocol

from backend.core.schemas import TaskContract
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tools import ToolResult


class AgentRuntime(ABC):
    """Framework-neutral interface for an agent runtime."""

    @abstractmethod
    def execute(
        self,
        task: TaskContract,
        tool_boundary: RuntimeToolBoundary,
    ) -> ToolResult:
        raise NotImplementedError


class ToolExecutor(Protocol):
    def execute_tool(self, name: str, arguments: Mapping[str, Any]) -> ToolResult:
        ...


class BoundaryToolExecutor:
    """Execute tools only through the authoritative runtime capability boundary."""

    def __init__(self, tool_boundary: RuntimeToolBoundary) -> None:
        self._tool_boundary = tool_boundary

    def execute_tool(self, name: str, arguments: Mapping[str, Any]) -> ToolResult:
        return self._tool_boundary.execute(name, arguments)
