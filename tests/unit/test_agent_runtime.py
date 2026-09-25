import pytest

from backend.core.agent_runtime import RegistryToolExecutor
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(name="echo", description="test tool")

    def run(self, arguments: dict[str, object]) -> ToolResult:
        return ToolResult(success=True, output=arguments)


def test_registry_tool_executor_uses_registered_tool() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())
    executor = RegistryToolExecutor(registry)

    result = executor.execute_tool("echo", {"value": 1})

    assert result.success
    assert result.output == {"value": 1}


def test_registry_tool_executor_fails_closed_for_unknown_tool() -> None:
    executor = RegistryToolExecutor(ToolRegistry())

    with pytest.raises(KeyError):
        executor.execute_tool("missing", {})
