from typing import Any

from backend.core.tools import Tool, ToolMetadata, ToolResult
from backend.local_agent.broker import LocalCapabilityBroker, LocalCapabilityDenied


class LocalFilesystemReadTool(Tool):
    """Expose only the broker's read-only filesystem capability to the runtime."""

    metadata = ToolMetadata(
        name="filesystem.read_text",
        description="Read UTF-8 text from explicitly configured local roots",
        risk_level="medium",
    )

    def __init__(self, broker: LocalCapabilityBroker) -> None:
        self._broker = broker

    def run(self, arguments: dict[str, Any]) -> ToolResult:
        try:
            path = arguments.get("path")
            if not isinstance(path, str):
                raise ValueError("path must be a string")
            return ToolResult(
                success=True,
                output=self._broker.execute("read_text", {"path": path}),
            )
        except (LocalCapabilityDenied, ValueError) as exc:
            return ToolResult(success=False, error=str(exc))
