from backend.core.run_lifecycle import RunStatus
from backend.core.state_store import RunState, SQLiteRunStateStore


class RunManager:
    """Resume non-terminal persisted runs without re-executing completed work."""

    def __init__(self, store: SQLiteRunStateStore) -> None:
        self._store = store

    def resume(self, run_id: str) -> RunState:
        state = self._store.get(run_id)
        if state is None:
            raise KeyError("run not found")
        status = RunStatus(state.status)
        if status in {RunStatus.SUCCEEDED, RunStatus.FAILED, RunStatus.CANCELLED}:
            raise ValueError("terminal runs cannot be resumed")
        if status is RunStatus.CREATED:
            resumed = RunState(state.run_id, RunStatus.RUNNING.value, state.payload)
            self._store.save(resumed)
            return resumed
        return state
