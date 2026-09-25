from collections import deque
from dataclasses import dataclass
from threading import Lock
from time import time
from uuid import UUID

_SECRET_KEYS = {"password", "passwd", "token", "secret", "api_key", "authorization", "cookie"}


@dataclass(frozen=True)
class ExecutionEvent:
    sequence: int
    run_id: UUID
    kind: str
    detail: str
    timestamp: float


class ExecutionEventBus:
    def __init__(self, *, max_events_per_run: int = 200, max_runs: int = 1_000) -> None:
        if max_events_per_run < 1 or max_events_per_run > 10_000:
            raise ValueError("max_events_per_run must be between 1 and 10000")
        if max_runs < 1 or max_runs > 100_000:
            raise ValueError("max_runs must be between 1 and 100000")
        self._max = max_events_per_run
        self._max_runs = max_runs
        self._lock = Lock()
        self._next = 0
        self._events: dict[UUID, deque[ExecutionEvent]] = {}

    @staticmethod
    def _safe_detail(detail: str) -> str:
        lowered = detail.lower()
        if any(key in lowered for key in _SECRET_KEYS):
            return "[redacted]"
        return detail

    def publish(self, run_id: UUID, kind: str, detail: str = "") -> ExecutionEvent:
        if not kind or len(kind) > 100 or len(detail) > 2_000:
            raise ValueError("event fields exceed limits")
        with self._lock:
            self._next += 1
            if run_id not in self._events and len(self._events) >= self._max_runs:
                oldest_run = next(iter(self._events))
                del self._events[oldest_run]
            event = ExecutionEvent(self._next, run_id, kind, self._safe_detail(detail), time())
            self._events.setdefault(run_id, deque(maxlen=self._max)).append(event)
            return event

    def since(self, run_id: UUID, after: int = 0, limit: int = 100) -> list[ExecutionEvent]:
        if after < 0 or limit < 1 or limit > 100:
            raise ValueError("invalid event query")
        with self._lock:
            return [event for event in self._events.get(run_id, ()) if event.sequence > after][:limit]
