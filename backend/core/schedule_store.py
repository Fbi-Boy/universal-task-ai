import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

@dataclass(frozen=True)
class ScheduleRecord:
    schedule_id: str
    task_payload: str
    next_run_at: str
    status: str = "active"

class ScheduleStore:
    def __init__(self, path: Path):
        self.path = path
        with sqlite3.connect(self.path) as c:
            c.execute("CREATE TABLE IF NOT EXISTS schedules (schedule_id TEXT PRIMARY KEY, task_payload TEXT NOT NULL, next_run_at TEXT NOT NULL, status TEXT NOT NULL)")
            c.execute("CREATE TABLE IF NOT EXISTS schedule_claims (schedule_id TEXT PRIMARY KEY, claimed_at TEXT NOT NULL)")
    def upsert(self, record: ScheduleRecord):
        with sqlite3.connect(self.path) as c:
            c.execute("INSERT INTO schedules(schedule_id,task_payload,next_run_at,status) VALUES(?,?,?,?) ON CONFLICT(schedule_id) DO UPDATE SET task_payload=excluded.task_payload,next_run_at=excluded.next_run_at,status=excluded.status",(record.schedule_id,record.task_payload,record.next_run_at,record.status))
    def due(self, now: datetime):
        value=now.astimezone(timezone.utc).isoformat()
        with sqlite3.connect(self.path) as c:
            rows=c.execute("SELECT schedule_id,task_payload,next_run_at,status FROM schedules WHERE status='active' AND next_run_at<=? ORDER BY next_run_at,schedule_id",(value,)).fetchall()
        return [ScheduleRecord(*row) for row in rows]
    def claim(self, schedule_id: str, now: datetime):
        value=now.astimezone(timezone.utc).isoformat()
        with sqlite3.connect(self.path) as c:
            try:
                c.execute("INSERT INTO schedule_claims(schedule_id,claimed_at) VALUES(?,?)",(schedule_id,value))
                return True
            except sqlite3.IntegrityError:
                return False
    def complete_claim(self, schedule_id: str):
        with sqlite3.connect(self.path) as c:
            c.execute("DELETE FROM schedule_claims WHERE schedule_id=?",(schedule_id,))
