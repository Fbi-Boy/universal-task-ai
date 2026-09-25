import os
import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from backend.core.state_store import SQLiteRunStateStore

router = APIRouter(prefix="/v1/runs", tags=["runs"])
_store = SQLiteRunStateStore(Path(os.environ.get("UTA_RUN_STATE_DB", "/data/runs.sqlite3")))


@router.get("")
def list_runs(limit: int = Query(default=50, ge=1, le=100)):
    try:
        return _store.list(limit=limit)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=503, detail="run history unavailable") from exc


@router.get("/{run_id}")
def get_run(run_id: str):
    try:
        state = _store.get(run_id)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=503, detail="run history unavailable") from exc
    if state is None:
        raise HTTPException(status_code=404, detail="run not found")
    return state
