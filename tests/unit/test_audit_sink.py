from pathlib import Path
from uuid import uuid4

from backend.core.audit import AuditEvent
from backend.core.audit_sink import SQLiteAuditSink


def test_audit_sink_persists_sanitized_event(tmp_path: Path) -> None:
    sink = SQLiteAuditSink(tmp_path / "audit.db")
    event = AuditEvent(
        event_type="task_started",
        task_id=uuid4(),
        metadata={"safe": "ok", "token": "do-not-store"},
    )
    sink.append(event)
    assert sink.count() == 1
    row = sink._conn.execute("SELECT metadata FROM audit_events").fetchone()
    assert '"safe":"ok"' in row[0]
    assert "do-not-store" not in row[0]
    sink.close()
