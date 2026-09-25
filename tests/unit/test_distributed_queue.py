import json

import pytest

from backend.core.distributed_queue import Job, RedisJobQueue


class FakeRedis:
    def __init__(self):
        self.ready = []
        self.processing = []

    def eval(self, script, keys, ready_key, encoded, max_jobs):
        if len(self.ready) >= int(max_jobs):
            return 0
        self.ready.append(encoded)
        return 1

    def blmove(self, src, dst, timeout, *, src=None, dest=None):
        if not self.ready:
            return None
        value = self.ready.pop(0)
        self.processing.append(value)
        return value

    def lrem(self, key, count, value):
        values = self.processing
        if value in values:
            values.remove(value)
            return 1
        return 0


def test_queue_is_bounded_and_distributed_claim_is_ackable():
    queue = RedisJobQueue(FakeRedis(), max_jobs=1)
    job = Job("job-1", {"task": "hello"})
    assert queue.enqueue(job)
    assert not queue.enqueue(Job("job-2", {"task": "later"}))
    claimed = queue.claim(timeout_seconds=1)
    assert claimed == job
    queue.ack(claimed)


def test_queue_rejects_oversized_payload():
    queue = RedisJobQueue(FakeRedis(), max_payload_bytes=256)
    with pytest.raises(ValueError, match="exceeds"):
        queue.enqueue(Job("x", {"data": "a" * 1000}))


def test_distributed_queue_requires_tls_url():
    with pytest.raises(ValueError, match="rediss"):
        RedisJobQueue.from_url("redis://localhost:6379/0")


def test_queue_serialization_is_json_only():
    fake = FakeRedis()
    queue = RedisJobQueue(fake)
    queue.enqueue(Job("job-1", {"nested": {"value": 1}}))
    assert json.loads(fake.ready[0])["job_id"] == "job-1"
