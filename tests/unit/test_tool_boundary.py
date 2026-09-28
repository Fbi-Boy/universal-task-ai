from typing import Any, Mapping

import math
import pytest

from backend.core.permissions import ToolPermission
from backend.core.tool_boundary import RuntimeToolBoundary, ToolBoundaryDenied
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(name="safe.echo", description="test echo")

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        return ToolResult(success=True, output=dict(arguments))


class TrackingTool(Tool):
    metadata = ToolMetadata(name="safe.tracking", description="test tracking")

    def __init__(self) -> None:
        self.calls = 0

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        self.calls += 1
        return ToolResult(success=True, output="ran")


class UnregisteredTool(Tool):
    metadata = ToolMetadata(name="safe.echo", description="unregistered lookalike")

    def __init__(self) -> None:
        self.calls = 0

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        self.calls += 1
        return ToolResult(success=True, output="unregistered")


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


def test_boundary_reports_approval_requirement_without_executing():
    registry = ToolRegistry()
    registry.register(ApprovalTool())
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"message.send"})))
    assert boundary.requires_approval("message.send") is True


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


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_boundary_rejects_invalid_arguments_before_tool_runs(value: float):
    tool = TrackingTool()
    registry = ToolRegistry()
    registry.register(tool)
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"safe.tracking"})))
    with pytest.raises(ValueError, match="non-finite"):
        boundary.execute("safe.tracking", {"value": value})
    assert tool.calls == 0


def test_boundary_rejects_unregistered_tool_instance_even_if_name_matches():
    registered = EchoTool()
    impostor = UnregisteredTool()
    registry = ToolRegistry()
    registry.register(registered)
    boundary = RuntimeToolBoundary(registry, ToolPermission(frozenset({"safe.echo"})))
    with pytest.raises(ToolBoundaryDenied, match="not the registered implementation"):
        boundary.execute_authorized(impostor, {})
    assert impostor.calls == 0
