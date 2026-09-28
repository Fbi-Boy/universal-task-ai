from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

from backend.core.audit import AuditEvent
from backend.core.audit_sink import SQLiteAuditSink
from backend.core.state_store import RunState, SQLiteRunStateStore


def test_run_state_store_supports_worker_threads(tmp_path: Path) -> None:
    store = SQLiteRunStateStore(tmp_path / "runs.sqlite3")

    def write(index: int) -> None:
        store.save(RunState(f"run-{index}", "succeeded", "{}"))
        store.ping()
        assert store.get(f"run-{index}") is not None

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(write, range(32)))

    assert len(store.list(limit=50)) == 32


def test_audit_sink_supports_worker_threads(tmp_path: Path) -> None:
    sink = SQLiteAuditSink(tmp_path / "audit.sqlite3")

    def append(index: int) -> None:
        sink.append(
            AuditEvent(
                event_type="task_started",
                task_id=uuid4(),
                metadata={"worker_index": index},
            )
        )
        sink.ping()

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(append, range(32)))

    assert sink.count() == 32
    sink.close()
