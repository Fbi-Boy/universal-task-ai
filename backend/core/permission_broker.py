from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True)
class PermissionGrant:
    grant_id: UUID
    task_id: UUID
    capabilities: frozenset[str]
    expires_at: datetime

    def active(self, now: datetime | None = None) -> bool:
        current = now or datetime.now(timezone.utc)
        return current < self.expires_at


class PermissionBroker:
    """Fail-closed capability broker for local execution authority."""

    def __init__(self) -> None:
        self._grants: dict[UUID, PermissionGrant] = {}

    def grant(
        self,
        task_id: UUID,
        capabilities: frozenset[str],
        *,
        ttl_seconds: int = 300,
    ) -> PermissionGrant:
        if not capabilities:
            raise ValueError("at least one capability is required")
        if ttl_seconds < 1 or ttl_seconds > 3600:
            raise ValueError("ttl_seconds must be between 1 and 3600")
        normalized = frozenset(cap.strip() for cap in capabilities if cap.strip())
        if not normalized:
            raise ValueError("capabilities must not be blank")
        grant = PermissionGrant(
            grant_id=uuid4(),
            task_id=task_id,
            capabilities=normalized,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds),
        )
        self._grants[grant.grant_id] = grant
        return grant

    def revoke(self, grant_id: UUID) -> None:
        self._grants.pop(grant_id, None)

    def authorize(
        self,
        grant_id: UUID,
        task_id: UUID,
        capability: str,
        *,
        now: datetime | None = None,
    ) -> None:
        grant = self._grants.get(grant_id)
        if grant is None:
            raise PermissionError("permission grant not found")
        if grant.task_id != task_id:
            raise PermissionError("permission grant is not bound to task")
        if not grant.active(now):
            raise PermissionError("permission grant expired")
        if capability not in grant.capabilities:
            raise PermissionError("capability not granted")
