import os
import pytest
from fastapi import HTTPException

from backend.api.auth import require_configured_api_key


def test_missing_environment_key_fails_closed(monkeypatch) -> None:
    monkeypatch.delenv("UNIVERSAL_TASK_AI_API_KEY", raising=False)
    with pytest.raises(HTTPException) as exc:
        require_configured_api_key("Bearer anything")
    assert exc.value.status_code == 503


def test_environment_key_authenticates(monkeypatch) -> None:
    monkeypatch.setenv("UNIVERSAL_TASK_AI_API_KEY", "test-key")
    require_configured_api_key("Bearer test-key")
