from backend.core.schedule_store import ScheduleStore
from backend.core.scheduler_worker import SchedulerWorker

class ScheduleTaskPipeline:
    def __init__(self,store:ScheduleStore,task_dispatcher):
        self.worker=SchedulerWorker(store,task_dispatcher)
    def tick(self,now):
        return self.worker.poll_once(now)
