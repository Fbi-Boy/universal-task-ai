from dataclasses import dataclass
from time import time

@dataclass(frozen=True)
class IdempotencyRecord:
    key: str
    created_at: float
    result_id: str

class ChannelIdempotencyStore:
    def __init__(self, ttl_seconds=86400):
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.ttl_seconds = ttl_seconds
        self._records = {}

    def claim(self, key: str, result_id: str, now=None):
        if not key or len(key) > 256 or not result_id or len(result_id) > 256:
            raise ValueError("invalid idempotency key or result")
        now = time() if now is None else now
        record = self._records.get(key)
        if record and now - record.created_at < self.ttl_seconds:
            return False, record
        record = IdempotencyRecord(key, now, result_id)
        self._records[key] = record
        return True, record

    def purge(self, now=None):
        now = time() if now is None else now
        self._records = {
            k: v for k, v in self._records.items()
            if now - v.created_at < self.ttl_seconds
        }
