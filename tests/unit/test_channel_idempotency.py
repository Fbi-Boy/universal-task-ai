from backend.channels.idempotency import ChannelIdempotencyStore

def test_duplicate_is_rejected_until_ttl():
    s = ChannelIdempotencyStore(10)
    assert s.claim("wa:1", "run-1", now=100)[0]
    assert not s.claim("wa:1", "run-2", now=105)[0]
    assert s.claim("wa:1", "run-3", now=111)[0]

def test_invalid_key_is_rejected():
    s = ChannelIdempotencyStore()
    try:
        s.claim("", "run")
        assert False
    except ValueError:
        assert True
