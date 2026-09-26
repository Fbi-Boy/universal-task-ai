import pytest


def test_python_sandbox_is_disabled_by_default(monkeypatch) -> None:
    from backend.core.runtime_tools import build_runtime_tool_boundary

    monkeypatch.delenv("UTA_PYTHON_SANDBOX_ENABLED", raising=False)
    monkeypatch.delenv("UTA_SANDBOX_IMAGE", raising=False)
    boundary = build_runtime_tool_boundary()
    assert "python_sandbox" not in boundary.allowed_tools()


def test_python_sandbox_requires_immutable_image(monkeypatch) -> None:
    from backend.core.runtime_tools import build_runtime_tool_boundary

    monkeypatch.setenv("UTA_PYTHON_SANDBOX_ENABLED", "true")
    monkeypatch.setenv("UTA_SANDBOX_IMAGE", "python:3.11")
    with pytest.raises(ValueError, match="immutable sha256 digest"):
        build_runtime_tool_boundary()
