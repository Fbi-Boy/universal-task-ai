from pathlib import Path

from backend.core.runtime_tools import build_runtime_tool_boundary

def test_project_context_capability_is_opt_in_with_local_roots(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("UTA_LOCAL_ROOTS", str(tmp_path))
    boundary = build_runtime_tool_boundary()
    assert "filesystem.project_context" in boundary.allowed_tools()

def test_project_context_capability_is_absent_without_local_roots(monkeypatch) -> None:
    monkeypatch.delenv("UTA_LOCAL_ROOTS", raising=False)
    boundary = build_runtime_tool_boundary()
    assert "filesystem.project_context" not in boundary.allowed_tools()
