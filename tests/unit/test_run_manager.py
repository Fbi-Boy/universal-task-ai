from pathlib import Path

import pytest

from backend.core.run_lifecycle import RunStatus
from backend.core.run_manager import RunManager
from backend.core.state_store import RunState, SQLiteRunStateStore


def test_created_run_resumes_to_running(tmp_path: Path) -> None:
    store = SQLiteRunStateStore(tmp_path / "runs.db")
    state = RunState("r1", RunStatus.CREATED.value, "{}")
    store.save(state)
    resumed = RunManager(store).resume("r1")
    assert resumed.status == RunStatus.RUNNING.value
    assert store.get("r1") == resumed


def test_running_and_waiting_runs_resume_idempotently(tmp_path: Path) -> None:
    store = SQLiteRunStateStore(tmp_path / "runs.db")
    manager = RunManager(store)
    for status in (RunStatus.RUNNING, RunStatus.WAITING_APPROVAL):
        state = RunState(status.value, status.value, "{}")
        store.save(state)
        assert manager.resume(state.run_id) == state


def test_terminal_runs_cannot_resume(tmp_path: Path) -> None:
    store = SQLiteRunStateStore(tmp_path / "runs.db")
    manager = RunManager(store)
    for status in (RunStatus.SUCCEEDED, RunStatus.FAILED, RunStatus.CANCELLED):
        state = RunState(status.value, status.value, "{}")
        store.save(state)
        with pytest.raises(ValueError):
            manager.resume(state.run_id)
