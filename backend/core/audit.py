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

        def sanitize(value: Any) -> Any:
            if isinstance(value, dict):
                return {
                    str(key): sanitize(item)
                    for key, item in value.items()
                    if str(key).lower() not in blocked
                }
            if isinstance(value, list):
                return [sanitize(item) for item in value]
            if isinstance(value, tuple):
                return [sanitize(item) for item in value]
            return value

        return sanitize(self.metadata)
