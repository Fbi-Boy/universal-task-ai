from pathlib import Path

from backend.core.runtime_tools import build_runtime_tool_boundary


def test_runtime_keeps_local_capability_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("UTA_LOCAL_ROOTS", raising=False)
    monkeypatch.delenv("UTA_BROWSER_ENABLED", raising=False)
    boundary = build_runtime_tool_boundary()
    assert boundary.allowed_tools() == ("calculator",)


def test_runtime_adds_local_read_only_capability_when_configured(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("UTA_LOCAL_ROOTS", str(tmp_path))
    monkeypatch.delenv("UTA_BROWSER_ENABLED", raising=False)
    boundary = build_runtime_tool_boundary()
    assert boundary.allowed_tools() == ("calculator", "filesystem.read_text")
