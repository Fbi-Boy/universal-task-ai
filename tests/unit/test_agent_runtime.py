import pytest

from backend.core.agent_runtime import BoundaryToolExecutor
from backend.core.permissions import ToolPermission
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(name="echo", description="test tool")

    def run(self, arguments: dict[str, object]) -> ToolResult:
        return ToolResult(success=True, output=arguments)


class ApprovalTool(Tool):
    metadata = ToolMetadata(
        name="message.send",
        description="approval-required test tool",
        requires_approval=True,
    )

    def run(self, arguments: dict[str, object]) -> ToolResult:
        return ToolResult(success=True, output=arguments)


def test_boundary_tool_executor_uses_registered_tool() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())
    boundary = RuntimeToolBoundary(
        registry,
        ToolPermission(frozenset({"echo"})),
    )
    executor = BoundaryToolExecutor(boundary)

    result = executor.execute_tool("echo", {"value": 1})

    assert result.success
    assert result.output == {"value": 1}


def test_boundary_tool_executor_fails_closed_for_unknown_tool() -> None:
    boundary = RuntimeToolBoundary(ToolRegistry(), ToolPermission(frozenset()))
    executor = BoundaryToolExecutor(boundary)

    with pytest.raises(PermissionError):
        executor.execute_tool("missing", {})


def test_boundary_tool_executor_cannot_bypass_capability_policy() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset()))
    executor = BoundaryToolExecutor(boundary)

    with pytest.raises(PermissionError):
        executor.execute_tool("echo", {})


def test_boundary_tool_executor_cannot_bypass_approval() -> None:
    registry = ToolRegistry()
    registry.register(ApprovalTool())
    boundary = RuntimeToolBoundary(
        registry,
        ToolPermission(frozenset({"message.send"})),
    )
    executor = BoundaryToolExecutor(boundary)

    with pytest.raises(PermissionError):
        executor.execute_tool("message.send", {})
