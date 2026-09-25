from pathlib import Path


from backend.api import runs
from backend.core.state_store import RunState, SQLiteRunStateStore


def test_list_runs_is_bounded(monkeypatch, tmp_path: Path) -> None:
    store = SQLiteRunStateStore(tmp_path / "runs.db")
    store.save(RunState("a", "succeeded", "{}"))
    store.save(RunState("b", "failed", "{}"))
    monkeypatch.setattr(runs, "_store", store)
    result = runs.list_runs(limit=1)
    assert len(result) == 1


def test_get_missing_run_is_404(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(runs, "_store", SQLiteRunStateStore(tmp_path / "runs.db"))
    try:
        runs.get_run("missing")
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 404
    else:
        raise AssertionError("missing run should raise 404")
