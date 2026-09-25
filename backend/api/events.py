from uuid import UUID

from fastapi import APIRouter, Query

from backend.core.events import ExecutionEventBus

router = APIRouter(prefix="/v1/runs", tags=["runs"])
bus = ExecutionEventBus()


@router.get("/{run_id}/events")
def get_events(run_id: UUID, after: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=100)):
    return bus.since(run_id, after=after, limit=limit)
