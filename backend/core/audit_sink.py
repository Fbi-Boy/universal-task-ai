import json
import sqlite3
from pathlib import Path
from typing import Any

from backend.core.audit import AuditEvent


class SQLiteAuditSink:
    """Append-only SQLite sink for sanitized audit events."""

    def __init__(self, path: Path) -> None:
        self._conn = sqlite3.connect(path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS audit_events ("
            "event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, task_id TEXT NOT NULL, "
            "timestamp TEXT NOT NULL, actor TEXT NOT NULL, tool_name TEXT, success INTEGER, metadata TEXT NOT NULL)"
        )
        self._conn.commit()

    def append(self, event: AuditEvent) -> None:
        metadata = event.safe_metadata()
        self._conn.execute(
            "INSERT INTO audit_events(event_id,event_type,task_id,timestamp,actor,tool_name,success,metadata) "
            "VALUES(?,?,?,?,?,?,?,?)",
            (
                str(event.event_id), event.event_type, str(event.task_id), event.timestamp.isoformat(),
                event.actor, event.tool_name, None if event.success is None else int(event.success),
                json.dumps(metadata, sort_keys=True, separators=(",", ":")),
            ),
        )
        self._conn.commit()

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) FROM audit_events").fetchone()
        return int(row[0])

    def close(self) -> None:
        self._conn.close()


class InMemoryAuditSink:
    """Test-friendly audit sink with the same append contract."""

    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(
            event.model_copy(update={"metadata": event.safe_metadata()})
        )
