from pathlib import Path
from uuid import uuid4

from backend.core.jobs import BackgroundJobRunner
from backend.core.memory import MemoryStore
from backend.core.retention import RetentionPolicy
from backend.core.state_store import RunState, SQLiteRunStateStore


def test_sqlite_run_state_roundtrip(tmp_path: Path) -> None:
    store = SQLiteRunStateStore(tmp_path / "runs.db")
    state = RunState(str(uuid4()), "running", "{}")
    store.save(state)
    assert store.get(state.run_id) == state


def test_memory_store() -> None:
    store = MemoryStore()
    store.put("k", "v")
    assert store.get("k").value == "v"
    store.delete("k")
    assert store.get("k") is None


def test_retention_cutoff() -> None:
    assert RetentionPolicy(7).cutoff().tzinfo is not None


def test_background_job_runner() -> None:
    runner = BackgroundJobRunner()
    assert runner.submit(lambda: 42).result() == 42
    runner._executor.shutdown()
