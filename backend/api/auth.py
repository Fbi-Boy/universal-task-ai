import hmac
from dataclasses import dataclass

from fastapi import Header, HTTPException


@dataclass(frozen=True)
class AuthConfig:
    api_key: str


def require_api_key(config: AuthConfig, authorization: str | None = Header(default=None)) -> None:
    if not config.api_key:
        raise HTTPException(status_code=503, detail="authentication is not configured")
    expected = "Bearer " + config.api_key
    if authorization is None or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="authentication required", headers={"WWW-Authenticate": "Bearer"})
