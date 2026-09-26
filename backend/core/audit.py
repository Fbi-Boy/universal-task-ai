from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

AuditEventType = Literal["task_started", "tool_authorized", "tool_started", "tool_finished", "tool_denied", "approval_pending", "task_finished", "task_failed"]

class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: UUID = Field(default_factory=uuid4)
    event_type: AuditEventType
    task_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str = "orchestrator"
    tool_name: str | None = None
    success: bool | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def safe_metadata(self) -> dict[str, Any]:
        """Return metadata after removing obvious secret-bearing keys."""
        blocked = {"password", "token", "secret", "api_key", "authorization"}
        return {
            key: value
            for key, value in self.metadata.items()
            if key.lower() not in blocked
        }
