from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from backend.core.permission_broker import PermissionBroker


def test_grant_is_scoped_and_active() -> None:
    broker = PermissionBroker()
    task_id = uuid4()
    grant = broker.grant(task_id, frozenset({"filesystem.read"}), ttl_seconds=60)
    broker.authorize(grant.grant_id, task_id, "filesystem.read")


def test_wrong_task_and_capability_fail_closed() -> None:
    broker = PermissionBroker()
    task_id = uuid4()
    grant = broker.grant(task_id, frozenset({"filesystem.read"}))
    with pytest.raises(PermissionError):
        broker.authorize(grant.grant_id, uuid4(), "filesystem.read")
    with pytest.raises(PermissionError):
        broker.authorize(grant.grant_id, task_id, "filesystem.write")


def test_expired_and_revoked_grants_fail() -> None:
    broker = PermissionBroker()
    task_id = uuid4()
    grant = broker.grant(task_id, frozenset({"filesystem.read"}))
    future = grant.expires_at + timedelta(seconds=1)
    with pytest.raises(PermissionError):
        broker.authorize(grant.grant_id, task_id, "filesystem.read", now=future)
    broker.revoke(grant.grant_id)
    with pytest.raises(PermissionError):
        broker.authorize(grant.grant_id, task_id, "filesystem.read")


def test_ttl_bounds_are_enforced() -> None:
    broker = PermissionBroker()
    with pytest.raises(ValueError):
        broker.grant(uuid4(), frozenset({"x"}), ttl_seconds=0)
    with pytest.raises(ValueError):
        broker.grant(uuid4(), frozenset({"x"}), ttl_seconds=3601)
