from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


class SecretNotConfigured(RuntimeError):
    """Raised when a required secret is not available."""


@dataclass(frozen=True)
class SecretProvider:
    """Read secrets from a mounted secret file, with explicit env fallback.

    The provider never returns values through metadata or logging. Callers
    should keep the returned value in memory only for the operation requiring
    it. Secret names are fixed application configuration, not task input.
    """

    secret_dir: Path = Path("/run/secrets")
    allow_environment_fallback: bool = True

    def get(self, name: str, *, env_name: str | None = None, required: bool = True) -> str | None:
        if not name or "/" in name or "\\" in name or name in {".", ".."}:
            raise ValueError("invalid secret name")

        path = self.secret_dir / name
        if path.is_file():
            value = path.read_text(encoding="utf-8").strip()
            if value:
                return value

        if self.allow_environment_fallback and env_name:
            value = os.environ.get(env_name, "").strip()
            if value:
                return value

        if required:
            raise SecretNotConfigured(f"secret {name!r} is not configured")
        return None
