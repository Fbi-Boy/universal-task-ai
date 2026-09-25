from dataclasses import dataclass
from typing import FrozenSet

@dataclass(frozen=True)
class ToolPermission:
    allowed_tools: FrozenSet[str]
    allow_network: bool = False
    allow_filesystem: bool = False
    allow_process: bool = False

    def can_use(self, tool_name: str) -> bool:
        return tool_name in self.allowed_tools

    def validate_capabilities(
        self,
        *,
        needs_network: bool = False,
        needs_filesystem: bool = False,
        needs_process: bool = False,
    ) -> tuple[str, ...]:
        errors: list[str] = []
        if needs_network and not self.allow_network:
            errors.append("network capability is not permitted")
        if needs_filesystem and not self.allow_filesystem:
            errors.append("filesystem capability is not permitted")
        if needs_process and not self.allow_process:
            errors.append("process capability is not permitted")
        return tuple(errors)

class PermissionDenied(PermissionError):
    pass

def authorize_tool(
    permissions: ToolPermission,
    tool_name: str,
    *,
    needs_network: bool = False,
    needs_filesystem: bool = False,
    needs_process: bool = False,
) -> None:
    if not permissions.can_use(tool_name):
        raise PermissionDenied(f"tool is not permitted: {tool_name}")
    errors = permissions.validate_capabilities(
        needs_network=needs_network,
        needs_filesystem=needs_filesystem,
        needs_process=needs_process,
    )
    if errors:
        raise PermissionDenied("; ".join(errors))
