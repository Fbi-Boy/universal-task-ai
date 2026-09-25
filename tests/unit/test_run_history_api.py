from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.api import runs
from backend.core.state_store import RunState, SQLiteRunStateStore


def test_list_runs_is_bounded(monkeypatch, tmp_path: Path) -> None:
    store = SQLiteRunStateStore(tmp_path / "runs.db")
    store.save(RunState("a", "succeeded", "{}"))
    store.save(RunState("b", "failed", "{}"))
    monkeypatch.setattr(runs, "_store", store)
    app = FastAPI()
    app.include_router(runs.router)
    client = TestClient(app)
    response = client.get("/v1/runs?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_missing_run_is_404(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(runs, "_store", SQLiteRunStateStore(tmp_path / "runs.db"))
    app = FastAPI()
    app.include_router(runs.router)
    client = TestClient(app)
    assert client.get("/v1/runs/missing").status_code == 404
