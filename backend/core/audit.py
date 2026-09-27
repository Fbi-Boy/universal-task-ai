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
        """Recursively remove common secret-bearing keys before persistence/export."""
        blocked = {"password", "token", "secret", "api_key", "authorization", "cookie"}

        def sanitize(value: Any, depth: int = 0) -> Any:
            if depth > 8:
                return "[redacted: max audit depth]"
            if isinstance(value, dict):
                if len(value) > 128:
                    return "[redacted: audit mapping too large]"
                return {
                    str(key)[:128]: sanitize(item, depth + 1)
                    for key, item in value.items()
                    if str(key).lower() not in blocked
                }
            if isinstance(value, (list, tuple)):
                if len(value) > 128:
                    return "[redacted: audit collection too large]"
                return [sanitize(item, depth + 1) for item in value]
            if isinstance(value, (str, bytes)):
                if len(value) > 8 * 1024:
                    return "[redacted: audit scalar too large]"
            return value

        return sanitize(self.metadata)
