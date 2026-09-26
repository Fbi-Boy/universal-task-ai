from typing import Any
from backend.core.project_context import ProjectContextReader
from backend.core.tools import Tool, ToolMetadata, ToolResult

class ProjectContextTool(Tool):
    metadata = ToolMetadata(
        name="filesystem.project_context",
        description="Read bounded source files from an explicitly configured project workspace.",
        risk_level="low",
        requires_network=False,
        requires_approval=False,
    )

    def __init__(self, reader: ProjectContextReader) -> None:
        self._reader = reader

    def run(self, arguments: dict[str, Any]) -> ToolResult:
        paths = tuple(arguments.get("paths", ()))
        if not all(isinstance(path, str) for path in paths):
            return ToolResult(success=False, error="paths must be strings")
        context = self._reader.collect(paths)
        return ToolResult(
            success=True,
            output={
                "root": context.root,
                "files": [{"path": item.path, "content": item.content, "bytes": item.bytes} for item in context.files],
            },
        )
