from datetime import datetime,timezone
from backend.core.schedule_store import ScheduleRecord,ScheduleStore
from backend.core.scheduler_worker import SchedulerWorker

class Dispatcher:
    def __init__(self): self.tasks=[]
    def dispatch(self,payload): self.tasks.append(payload)

def test_worker_dispatches_due_schedule_once(tmp_path):
    store=ScheduleStore(tmp_path/"s.db")
    now=datetime.now(timezone.utc)
    store.upsert(ScheduleRecord("s1","task-1",now.isoformat()))
    d=Dispatcher()
    w=SchedulerWorker(store,d)
    assert w.poll_once(now)[0].schedule_id=="s1"
    assert d.tasks==["task-1"]
    assert w.poll_once(now)==[]
