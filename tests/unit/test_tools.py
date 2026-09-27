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


def test_tool_result_rejects_oversized_output():
    result = ToolResult(success=True, output="x" * (64 * 1024 + 1))
    with pytest.raises(ValueError, match="64 KiB"):
        result.validate_bounds()


def test_tool_result_rejects_deep_output():
    value = "ok"
    for _ in range(9):
        value = [value]
    result = ToolResult(success=True, output=value)
    with pytest.raises(ValueError, match="nesting depth"):
        result.validate_bounds()


def test_tool_result_rejects_oversized_error():
    result = ToolResult(success=False, error="x" * 2_001)
    with pytest.raises(ValueError, match="2000 characters"):
        result.validate_bounds()
