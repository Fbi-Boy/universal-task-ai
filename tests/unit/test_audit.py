from uuid import uuid4

from backend.core.audit import AuditEvent

def test_audit_event_has_stable_identity_and_timestamp():
    event = AuditEvent(event_type="task_started", task_id=uuid4())
    assert event.event_id
    assert event.timestamp.tzinfo is not None

def test_audit_metadata_redacts_secret_keys():
    event = AuditEvent(
        event_type="tool_started",
        task_id=uuid4(),
        metadata={"tool": "web", "api_key": "do-not-log", "safe": "ok"},
    )
    assert event.safe_metadata() == {"tool": "web", "safe": "ok"}


def test_audit_metadata_removes_nested_secret_keys():
    event = AuditEvent(
        event_type="tool_started",
        task_id=uuid4(),
        metadata={"request": {"authorization": "secret", "value": "ok"}},
    )
    assert event.safe_metadata() == {"request": {"value": "ok"}}


def test_audit_metadata_bounds_large_scalars_and_collections():
    event = AuditEvent(
        event_type="tool_started",
        task_id=uuid4(),
        metadata={"large": "x" * (8 * 1024 + 1), "items": list(range(129))},
    )
    safe = event.safe_metadata()
    assert safe["large"] == "[redacted: audit scalar too large]"
    assert safe["items"] == "[redacted: audit collection too large]"
