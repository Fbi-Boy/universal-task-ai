from pathlib import Path
from typing import Any

from backend.core.tools import Tool, ToolMetadata, ToolResult

_MAX_BYTES = 1_000_000


class FileReaderTool(Tool):
    metadata = ToolMetadata(
        name="file_reader",
        description="Read UTF-8 text only from an explicitly configured root directory.",
        risk_level="medium",
        requires_network=False,
        requires_approval=False,
    )

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def run(self, arguments: dict[str, Any]) -> ToolResult:
        relative = arguments.get("path")
        if not isinstance(relative, str) or not relative.strip():
            return ToolResult(success=False, error="path must be a non-empty string")
        raw_candidate = self._root / relative
        if raw_candidate.is_symlink():
            return ToolResult(success=False, error="symlink paths are not allowed")
        candidate = raw_candidate.resolve()
        try:
            candidate.relative_to(self._root)
        except ValueError:
            return ToolResult(success=False, error="path escapes configured root")
        if not candidate.is_file():
            return ToolResult(success=False, error="path is not an allowed regular file")
        try:
            if candidate.stat().st_size > _MAX_BYTES:
                return ToolResult(success=False, error="file exceeds size limit")
            return ToolResult(success=True, output=candidate.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            return ToolResult(success=False, error="file could not be read safely")
