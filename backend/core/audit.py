import re
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

AuditEventType = Literal["task_started", "tool_authorized", "tool_started", "tool_finished", "tool_denied", "approval_pending", "approval_consumed", "task_finished", "task_failed"]


class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: UUID = Field(default_factory=uuid4)
    event_type: AuditEventType
    task_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str = Field(default="orchestrator", min_length=1, max_length=128)
    tool_name: str | None = Field(default=None, max_length=128)
    success: bool | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def safe_metadata(self) -> dict[str, Any]:
        """Recursively bound metadata and redact common secret-bearing key variants."""
        blocked_parts = {
            "password", "passwd", "token", "secret", "key", "authorization",
            "cookie", "credential", "credentials", "bearer", "private",
        }
        blocked_phrases = {
            "api_key", "access_key", "private_key", "client_secret",
            "set_cookie", "access_token", "refresh_token", "id_token",
        }

        def is_secret_key(key: object) -> bool:
            raw = str(key)
            # Split camelCase and punctuation before checking key words.
            words = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", raw)
            words = re.sub(r"[^A-Za-z0-9]+", "_", words).lower().strip("_")
            parts = set(words.split("_")) if words else set()
            compact = words.replace("_", "")
            return bool(
                parts & blocked_parts
                or any(phrase in words for phrase in blocked_phrases)
                or compact in {"apikey", "accesskey", "privatekey", "clientsecret", "setcookie", "accesstoken", "refreshtoken", "idtoken"}
            )

        def sanitize(value: Any, depth: int = 0) -> Any:
            if depth > 8:
                return "[redacted: max audit depth]"
            if isinstance(value, dict):
                if len(value) > 128:
                    return "[redacted: audit mapping too large]"
                return {
                    str(key)[:128]: sanitize(item, depth + 1)
                    for key, item in value.items()
                    if not is_secret_key(key)
                }
            if isinstance(value, (list, tuple)):
                if len(value) > 128:
                    return "[redacted: audit collection too large]"
                return [sanitize(item, depth + 1) for item in value]
            if isinstance(value, (str, bytes)) and len(value) > 8 * 1024:
                return "[redacted: audit scalar too large]"
            return value

        return sanitize(self.metadata)
