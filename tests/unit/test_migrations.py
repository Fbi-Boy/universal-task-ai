from backend.core.migrations import migrate

def test_migrations_are_idempotent(tmp_path):
    path=tmp_path/"db.sqlite3"
    assert migrate(path)==2
    assert migrate(path)==2
