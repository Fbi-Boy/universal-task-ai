import sqlite3
from dataclasses import dataclass
from pathlib import Path
from time import time

@dataclass(frozen=True)
class DurableIdempotencyRecord:
    key: str
    created_at: float
    result_id: str

class SQLiteChannelIdempotencyStore:
    """Durable, atomic channel deduplication backed by SQLite."""
    def __init__(self, path: Path, ttl_seconds: int = 86400):
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.path = path
        self.ttl_seconds = ttl_seconds
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS channel_idempotency (key TEXT PRIMARY KEY, created_at REAL NOT NULL, result_id TEXT NOT NULL)")

    def claim(self, key: str, result_id: str, now: float | None = None):
        if not key or len(key) > 256 or not result_id or len(result_id) > 256:
            raise ValueError("invalid idempotency key or result")
        now = time() if now is None else now
        cutoff = now - self.ttl_seconds
        with sqlite3.connect(self.path) as db:
            db.execute("DELETE FROM channel_idempotency WHERE created_at < ?", (cutoff,))
            try:
                db.execute("INSERT INTO channel_idempotency(key,created_at,result_id) VALUES(?,?,?)", (key, now, result_id))
                return True, DurableIdempotencyRecord(key, now, result_id)
            except sqlite3.IntegrityError:
                row = db.execute("SELECT key,created_at,result_id FROM channel_idempotency WHERE key=?", (key,)).fetchone()
                if row is None:
                    raise RuntimeError("idempotency claim lost")
                return False, DurableIdempotencyRecord(*row)
