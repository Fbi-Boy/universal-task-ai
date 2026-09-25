from abc import ABC, abstractmethod
from typing import Any, Mapping, Protocol

from backend.core.schemas import TaskContract
from backend.core.tools import ToolRegistry, ToolResult


class AgentRuntime(ABC):
    """Framework-neutral interface for an agent runtime."""

    @abstractmethod
    def execute(
        self,
        task: TaskContract,
        tools: ToolRegistry,
    ) -> ToolResult:
        raise NotImplementedError


class ToolExecutor(Protocol):
    def execute_tool(self, name: str, arguments: Mapping[str, Any]) -> ToolResult:
        ...


class RegistryToolExecutor:
    """Minimal adapter that executes only registered tools."""

    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry

    def execute_tool(self, name: str, arguments: Mapping[str, Any]) -> ToolResult:
        tool = self._registry.get(name)
        return tool.run(arguments)
