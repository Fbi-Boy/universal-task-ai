import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunState:
    run_id: str
    status: str
    payload: str


class SQLiteRunStateStore:
    def __init__(self, path: Path) -> None:
        self._conn = sqlite3.connect(path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, status TEXT NOT NULL, payload TEXT NOT NULL)")
        self._conn.commit()

    def save(self, state: RunState) -> None:
        self._conn.execute(
            "INSERT INTO runs(run_id,status,payload) VALUES(?,?,?) ON CONFLICT(run_id) DO UPDATE SET status=excluded.status,payload=excluded.payload",
            (state.run_id, state.status, state.payload),
        )
        self._conn.commit()

    def get(self, run_id: str) -> RunState | None:
        row = self._conn.execute("SELECT run_id,status,payload FROM runs WHERE run_id=?", (run_id,)).fetchone()
        return RunState(*row) if row else None
