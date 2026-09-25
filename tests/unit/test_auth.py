import pytest
from fastapi import HTTPException

from backend.api.auth import AuthConfig, require_api_key


def test_valid_bearer_key() -> None:
    require_api_key(AuthConfig("secret"), "Bearer secret")


def test_missing_and_invalid_keys_fail() -> None:
    with pytest.raises(HTTPException) as missing:
        require_api_key(AuthConfig("secret"), None)
    assert missing.value.status_code == 401
    with pytest.raises(HTTPException) as invalid:
        require_api_key(AuthConfig("secret"), "Bearer wrong")
    assert invalid.value.status_code == 401


def test_auth_is_fail_closed_when_unconfigured() -> None:
    with pytest.raises(HTTPException) as exc:
        require_api_key(AuthConfig(""), "Bearer anything")
    assert exc.value.status_code == 503
