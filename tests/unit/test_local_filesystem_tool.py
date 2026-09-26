from pathlib import Path

from backend.core.permissions import ToolPermission
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tools import ToolRegistry
from backend.local_agent.broker import LocalCapabilityBroker, LocalCapabilityPolicy
from backend.tools.local_filesystem import LocalFilesystemReadTool


def test_local_filesystem_tool_is_read_only_and_bounded(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    (root / "note.txt").write_text("hello", encoding="utf-8")

    registry = ToolRegistry()
    registry.register(LocalFilesystemReadTool(LocalCapabilityBroker(LocalCapabilityPolicy((root,)))))
    boundary = RuntimeToolBoundary(
        registry,
        ToolPermission(frozenset({"filesystem.read_text"}), allow_filesystem=True),
    )

    result = boundary.execute("filesystem.read_text", {"path": "note.txt"})
    assert result.success and result.output == "hello"
