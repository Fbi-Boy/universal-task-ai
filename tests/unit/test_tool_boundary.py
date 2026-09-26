from typing import Any, Mapping

import pytest

from backend.core.permissions import ToolPermission
from backend.core.tool_boundary import RuntimeToolBoundary, ToolBoundaryDenied
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(name="safe.echo", description="test echo")

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        return ToolResult(success=True, output=dict(arguments))


class ApprovalTool(Tool):
    metadata = ToolMetadata(
        name="message.send",
        description="test message sender",
        requires_approval=True,
    )

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        return ToolResult(success=True, output="sent")


class NetworkTool(Tool):
    metadata = ToolMetadata(
        name="web.search",
        description="test network tool",
        requires_network=True,
    )

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        return ToolResult(success=True, output="network")


def test_boundary_executes_only_registered_and_permitted_tool():
    registry = ToolRegistry()
    registry.register(EchoTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"safe.echo"})))
    result = boundary.execute("safe.echo", {"value": "ok"})
    assert result.success is True


def test_boundary_denies_unregistered_tool():
    boundary = RuntimeToolBoundary(ToolRegistry(), ToolPermission(frozenset()))
    with pytest.raises(ToolBoundaryDenied):
        boundary.execute("unknown", {})


def test_boundary_requires_explicit_approval():
    registry = ToolRegistry()
    registry.register(ApprovalTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"message.send"})))
    with pytest.raises(ToolBoundaryDenied, match="approval"):
        boundary.execute("message.send", {})
    assert boundary.execute("message.send", {}, approved=True).success is True


def test_boundary_denies_network_without_capability():
    registry = ToolRegistry()
    registry.register(NetworkTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"web.search"})))
    with pytest.raises(ToolBoundaryDenied, match="network"):
        boundary.execute("web.search", {})
