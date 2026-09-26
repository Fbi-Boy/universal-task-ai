from datetime import datetime,timezone
from backend.core.schedule_store import ScheduleRecord,ScheduleStore
from backend.core.schedule_pipeline import ScheduleTaskPipeline

class D:
    def __init__(self): self.items=[]
    def dispatch(self,payload): self.items.append(payload)

def test_pipeline_uses_scheduler_worker(tmp_path):
    now=datetime.now(timezone.utc); store=ScheduleStore(tmp_path/"s.db")
    store.upsert(ScheduleRecord("1","normal-task",now.isoformat()))
    d=D(); assert ScheduleTaskPipeline(store,d).tick(now)
    assert d.items==["normal-task"]
