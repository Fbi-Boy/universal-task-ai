import importlib

def test_run_store_uses_configured_database_path(monkeypatch, tmp_path):
    path = tmp_path / "runs.sqlite3"
    monkeypatch.setenv("UTA_RUN_STATE_DB", str(path))
    import backend.api.runs as runs
    importlib.reload(runs)
    assert path.exists()
    runs._store._conn.close()
