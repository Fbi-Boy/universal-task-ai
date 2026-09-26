from pathlib import Path
import pytest
from backend.core.project_context import ProjectContextReader
from backend.core.workspace_policy import WorkspaceDenied, WorkspacePolicy

def test_collects_only_allowed_source_files(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("print('ok')", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("ignored", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=do-not-read", encoding="utf-8")
    context = ProjectContextReader(WorkspacePolicy((tmp_path,))).collect()
    assert [item.path for item in context.files] == ["main.py"]

def test_rejects_escape_path(tmp_path: Path) -> None:
    reader = ProjectContextReader(WorkspacePolicy((tmp_path,)))
    with pytest.raises(WorkspaceDenied):
        reader.collect(("../outside.py",))

def test_skips_oversized_files(tmp_path: Path) -> None:
    (tmp_path / "large.py").write_text("x" * 100, encoding="utf-8")
    reader = ProjectContextReader(WorkspacePolicy((tmp_path,), max_file_bytes=10))
    assert reader.collect().files == ()

def test_limits_discovery(tmp_path: Path) -> None:
    for index in range(5):
        (tmp_path / f"file{index}.py").write_text(str(index), encoding="utf-8")
    reader = ProjectContextReader(WorkspacePolicy((tmp_path,), max_files=2))
    assert len(reader.collect().files) == 2

def test_explicit_request_cannot_bypass_ignored_directories(tmp_path: Path) -> None:
    dependency = tmp_path / "node_modules"
    dependency.mkdir()
    (dependency / "package.py").write_text("secret-ish dependency", encoding="utf-8")
    reader = ProjectContextReader(WorkspacePolicy((tmp_path,)))
    assert reader.collect(("node_modules/package.py",)).files == ()


def test_rejects_nul_path(tmp_path: Path) -> None:
    reader = ProjectContextReader(WorkspacePolicy((tmp_path,)))
    with pytest.raises(ValueError, match="NUL"):
        reader.collect(("safe.py\x00evil",))
