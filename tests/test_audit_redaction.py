from uuid import uuid4

from backend.core.audit import AuditEvent


def make_event(metadata: dict) -> AuditEvent:
    return AuditEvent(event_type="task_started", task_id=uuid4(), metadata=metadata)


def test_safe_metadata_redacts_normalized_secret_key_variants_recursively() -> None:
    event = make_event(
        {
            "apiKey": "do-not-log-1",
            "refresh_token": "do-not-log-2",
            "AuthorizationHeader": "do-not-log-3",
            "nested": {
                "client-secret": "do-not-log-4",
                "Cookie": "do-not-log-5",
                "safe_label": "kept",
            },
        }
    )

    safe = event.safe_metadata()

    assert "apiKey" not in safe
    assert "refresh_token" not in safe
    assert "AuthorizationHeader" not in safe
    assert safe["nested"] == {"safe_label": "kept"}
    assert "do-not-log" not in repr(safe)


def test_safe_metadata_keeps_non_secret_metadata() -> None:
    event = make_event(
        {
            "run_id": "run-123",
            "duration_ms": 12,
            "result": {"status": "ok", "count": 2},
        }
    )

    assert event.safe_metadata() == {
        "run_id": "run-123",
        "duration_ms": 12,
        "result": {"status": "ok", "count": 2},
    }


def test_safe_metadata_bounds_large_values_and_deep_nesting() -> None:
    deep: dict[str, object] = {"leaf": "ok"}
    for index in range(10):
        deep = {f"level_{index}": deep}

    safe = make_event(
        {
            "large_value": "x" * (8 * 1024 + 1),
            "deep": deep,
        }
    ).safe_metadata()

    assert safe["large_value"] == "[redacted: audit scalar too large]"
    assert "[redacted: max audit depth]" in repr(safe["deep"])
