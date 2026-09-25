from pathlib import Path
import sqlite3

MIGRATIONS=((1,"CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY)"),(2,"CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, status TEXT NOT NULL, payload TEXT NOT NULL)"))

def migrate(path: Path) -> int:
    conn=sqlite3.connect(path)
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY)")
        current=conn.execute("SELECT COALESCE(MAX(version),0) FROM schema_version").fetchone()[0]
        for version,sql in MIGRATIONS:
            if version<=current: continue
            conn.execute(sql)
            conn.execute("INSERT INTO schema_version(version) VALUES(?)",(version,))
        conn.commit()
        return MIGRATIONS[-1][0]
    finally: conn.close()
