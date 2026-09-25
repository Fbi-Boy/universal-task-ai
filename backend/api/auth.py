import hmac
from dataclasses import dataclass

from backend.core.secret_provider import SecretProvider

from fastapi import Header, HTTPException
import os


@dataclass(frozen=True)
class AuthConfig:
    api_key: str


def configured_auth() -> AuthConfig:
    provider = SecretProvider()
    return AuthConfig(provider.get("universal_task_ai_api_key", env_name="UNIVERSAL_TASK_AI_API_KEY", required=False) or "")


def require_configured_api_key(authorization: str | None = Header(default=None)) -> None:
    require_api_key(configured_auth(), authorization)


def require_api_key(config: AuthConfig, authorization: str | None = Header(default=None)) -> None:
    if not config.api_key:
        raise HTTPException(status_code=503, detail="authentication is not configured")
    expected = "Bearer " + config.api_key
    if authorization is None or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="authentication required", headers={"WWW-Authenticate": "Bearer"})
