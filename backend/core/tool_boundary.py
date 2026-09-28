from typing import Any, Mapping

from backend.core.permissions import ToolPermission, authorize_tool
from backend.core.tool_invocation import ToolInvocation
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class ToolBoundaryDenied(PermissionError):
    """Raised when a runtime tool invocation violates a capability policy."""


class RuntimeToolBoundary:
    """Single policy gate between orchestration and registered tools."""

    def __init__(self, registry: ToolRegistry, permissions: ToolPermission) -> None:
        self._registry = registry
        self._permissions = permissions

    def authorize(self, name: str, *, approved: bool = False) -> Tool:
        """Resolve and authorize a tool without executing it."""
        try:
            tool = self._registry.get(name)
        except KeyError as exc:
            raise ToolBoundaryDenied(f"tool is not registered: {name}") from exc
        metadata = tool.metadata
        try:
            authorize_tool(
                self._permissions,
                metadata.name,
                needs_network=metadata.requires_network,
                needs_filesystem=metadata.name.startswith("filesystem."),
                needs_process=metadata.name.startswith("process."),
            )
        except PermissionError as exc:
            raise ToolBoundaryDenied(str(exc)) from exc
        if metadata.requires_approval and not approved:
            raise ToolBoundaryDenied(f"approval is required for tool: {name}")
        return tool

    def requires_approval(self, name: str) -> bool:
        """Return approval requirement after validating capability access."""
        tool = self.authorize(name, approved=True)
        return tool.metadata.requires_approval

    def execute_authorized(
        self,
        tool: Tool,
        arguments: Mapping[str, Any],
        *,
        approved: bool = False,
    ) -> ToolResult:
        """Revalidate registration, permissions, approval, and input before execution."""
        try:
            registered = self._registry.get(tool.metadata.name)
        except KeyError as exc:
            raise ToolBoundaryDenied("tool is not registered") from exc
        if registered is not tool:
            raise ToolBoundaryDenied("tool instance is not the registered implementation")

        authorized = self.authorize(tool.metadata.name, approved=approved)
        if authorized is not tool:
            raise ToolBoundaryDenied("tool authorization did not resolve the registered implementation")

        invocation = ToolInvocation(tool_name=tool.metadata.name, arguments=arguments)
        invocation.validate_bounds()
        result = tool.run(invocation.arguments)
        result.validate_bounds()
        return result

    def execute(
        self,
        name: str,
        arguments: Mapping[str, Any],
        *,
        approved: bool = False,
    ) -> ToolResult:
        tool = self.authorize(name, approved=approved)
        return self.execute_authorized(tool, arguments, approved=approved)

    def allowed_tools(self) -> tuple[str, ...]:
        return tuple(
            metadata.name
            for metadata in self._registry.metadata()
            if self._permissions.can_use(metadata.name)
        )

    def catalog(self) -> tuple[ToolMetadata, ...]:
        """Expose only metadata for tools already allowed by this boundary."""
        return tuple(
            metadata
            for metadata in self._registry.metadata()
            if self._permissions.can_use(metadata.name)
        )
