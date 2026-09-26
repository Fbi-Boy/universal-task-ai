from backend.channels.sqlite_idempotency import SQLiteChannelIdempotencyStore

def test_sqlite_claim_survives_new_store(tmp_path):
    path = tmp_path / "state.db"
    first = SQLiteChannelIdempotencyStore(path, 10)
    assert first.claim("wa:1", "run-1", now=100)[0]
    second = SQLiteChannelIdempotencyStore(path, 10)
    claimed, record = second.claim("wa:1", "run-2", now=105)
    assert not claimed and record.result_id == "run-1"

def test_expired_claim_can_be_reused(tmp_path):
    store = SQLiteChannelIdempotencyStore(tmp_path / "state.db", 10)
    assert store.claim("wa:1", "run-1", now=100)[0]
    assert store.claim("wa:1", "run-2", now=111)[0]

def test_invalid_values_rejected(tmp_path):
    store = SQLiteChannelIdempotencyStore(tmp_path / "state.db")
    try:
        store.claim("", "run")
        assert False
    except ValueError:
        assert True
