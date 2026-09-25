import json
from dataclasses import dataclass
from typing import Any

import redis


@dataclass(frozen=True)
class Job:
    job_id: str
    payload: dict[str, Any]


_ENQUEUE_LUA = """
local current = redis.call('LLEN', KEYS[1])
if current >= tonumber(ARGV[2]) then
  return 0
end
redis.call('RPUSH', KEYS[1], ARGV[1])
return 1
"""


class RedisJobQueue:
    """Bounded Redis-backed queue shared by multiple workers.

    Jobs are moved atomically from ready -> processing. Acknowledgement
    removes only the claimed serialized job. The queue stores JSON only and
    never accepts executable payloads.
    """

    def __init__(
        self,
        client: redis.Redis,
        *,
        ready_key: str = "uta:jobs:ready",
        processing_key: str = "uta:jobs:processing",
        max_jobs: int = 1000,
        max_payload_bytes: int = 64 * 1024,
    ) -> None:
        if not ready_key or not processing_key or ready_key == processing_key:
            raise ValueError("invalid queue keys")
        if not 1 <= max_jobs <= 100_000:
            raise ValueError("max_jobs out of bounds")
        if not 256 <= max_payload_bytes <= 1_048_576:
            raise ValueError("max_payload_bytes out of bounds")
        self._client = client
        self._ready_key = ready_key
        self._processing_key = processing_key
        self._max_jobs = max_jobs
        self._max_payload_bytes = max_payload_bytes

    @classmethod
    def from_url(cls, url: str, **kwargs: Any) -> "RedisJobQueue":
        if not isinstance(url, str) or not url.startswith("rediss://"):
            raise ValueError("distributed Redis queue requires rediss://")
        return cls(redis.Redis.from_url(url, decode_responses=True), **kwargs)

    def enqueue(self, job: Job) -> bool:
        if not job.job_id or len(job.job_id) > 200:
            raise ValueError("invalid job id")
        encoded = json.dumps(
            {"job_id": job.job_id, "payload": job.payload},
            separators=(",", ":"),
            sort_keys=True,
            ensure_ascii=False,
        )
        if len(encoded.encode("utf-8")) > self._max_payload_bytes:
            raise ValueError("job payload exceeds queue limit")
        accepted = self._client.eval(
            _ENQUEUE_LUA,
            1,
            self._ready_key,
            encoded,
            self._max_jobs,
        )
        return bool(accepted)

    def claim(self, *, timeout_seconds: int = 5) -> Job | None:
        if not 1 <= timeout_seconds <= 60:
            raise ValueError("timeout out of bounds")
        encoded = self._client.blmove(
            self._ready_key,
            self._processing_key,
            timeout=timeout_seconds,
            src="LEFT",
            dest="RIGHT",
        )
        if encoded is None:
            return None
        try:
            item = json.loads(encoded)
            job_id, payload = item["job_id"], item["payload"]
            if not isinstance(job_id, str) or not isinstance(payload, dict):
                raise ValueError
            return Job(job_id=job_id, payload=payload)
        except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
            self._client.lrem(self._processing_key, 1, encoded)
            raise RuntimeError("invalid queued job") from exc

    def ack(self, job: Job) -> None:
        encoded = json.dumps(
            {"job_id": job.job_id, "payload": job.payload},
            separators=(",", ":"),
            sort_keys=True,
            ensure_ascii=False,
        )
        removed = self._client.lrem(self._processing_key, 1, encoded)
        if removed != 1:
            raise RuntimeError("job acknowledgement failed")
