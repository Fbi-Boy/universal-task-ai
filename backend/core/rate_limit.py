from dataclasses import dataclass
from time import monotonic
from threading import Lock


@dataclass(frozen=True)
class RateLimit:
    max_requests: int
    window_seconds: float

    def __post_init__(self) -> None:
        if self.max_requests < 1 or self.max_requests > 100_000:
            raise ValueError("max_requests must be between 1 and 100000")
        if self.window_seconds <= 0 or self.window_seconds > 86_400:
            raise ValueError("window_seconds must be > 0 and <= 86400")


class RateLimiter:
    """Thread-safe fixed-window limiter. Denies when the local store is unavailable."""

    def __init__(self, limit: RateLimit) -> None:
        self._limit = limit
        self._lock = Lock()
        self._windows: dict[str, tuple[float, int]] = {}

    def allow(self, key: str, *, now: float | None = None) -> bool:
        if not key or len(key) > 256:
            return False
        current = monotonic() if now is None else now
        with self._lock:
            start, count = self._windows.get(key, (current, 0))
            if current < start or current - start >= self._limit.window_seconds:
                start, count = current, 0
            if count >= self._limit.max_requests:
                self._windows[key] = (start, count)
                return False
            self._windows[key] = (start, count + 1)
            return True

    def reset(self, key: str) -> None:
        with self._lock:
            self._windows.pop(key, None)
