import pytest

from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult

class EchoTool(Tool):
    metadata = ToolMetadata(name="echo", description="return input")

    def run(self, arguments):
        return ToolResult(success=True, output=dict(arguments))

def test_registry_registers_and_resolves_tool():
    registry = ToolRegistry()
    tool = EchoTool()
    registry.register(tool)
    assert registry.get("echo") is tool

def test_registry_rejects_duplicate_tool_names():
    registry = ToolRegistry()
    registry.register(EchoTool())
    with pytest.raises(ValueError):
        registry.register(EchoTool())

def test_unknown_tool_fails_closed():
    with pytest.raises(KeyError):
        ToolRegistry().get("missing")
