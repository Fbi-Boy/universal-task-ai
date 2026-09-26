from datetime import datetime, timezone, timedelta
from backend.core.schedule_store import ScheduleRecord, ScheduleStore

def test_store_returns_due_records(tmp_path):
    s=ScheduleStore(tmp_path/"s.db"); now=datetime.now(timezone.utc)
    s.upsert(ScheduleRecord("a","task",(now-timedelta(seconds=1)).isoformat()))
    s.upsert(ScheduleRecord("b","task",(now+timedelta(seconds=60)).isoformat()))
    assert [x.schedule_id for x in s.due(now)] == ["a"]

def test_claim_is_idempotent(tmp_path):
    s=ScheduleStore(tmp_path/"s.db"); now=datetime.now(timezone.utc)
    assert s.claim("a",now)
    assert not s.claim("a",now)
    s.complete_claim("a")
    assert s.claim("a",now)
