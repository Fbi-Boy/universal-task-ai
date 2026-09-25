import math
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

_WORD = re.compile(r"[a-zA-Z0-9_]{2,}")

@dataclass(frozen=True)
class SemanticMemory:
    memory_id: int
    user_id: str
    text: str
    metadata: str

class SQLiteSemanticMemoryStore:
    def __init__(self, path: Path) -> None:
        self._conn = sqlite3.connect(path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("CREATE TABLE IF NOT EXISTS memories (memory_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, text TEXT NOT NULL, metadata TEXT NOT NULL)")
        self._conn.commit()

    @staticmethod
    def _vector(text: str) -> dict[str, float]:
        counts: dict[str, float] = {}
        for word in _WORD.findall(text.lower()): counts[word] = counts.get(word, 0.0) + 1.0
        norm = math.sqrt(sum(v * v for v in counts.values())) or 1.0
        return {k: v / norm for k, v in counts.items()}

    def put(self, user_id: str, text: str, metadata: str = "") -> int:
        if not user_id.strip() or not text.strip() or len(text) > 20_000 or len(metadata) > 10_000:
            raise ValueError("invalid memory")
        cur = self._conn.execute("INSERT INTO memories(user_id,text,metadata) VALUES(?,?,?)", (user_id, text, metadata))
        self._conn.commit()
        return int(cur.lastrowid)

    def search(self, user_id: str, query: str, *, limit: int = 10) -> list[tuple[SemanticMemory, float]]:
        if not user_id.strip() or not query.strip() or limit < 1 or limit > 50: raise ValueError("invalid search")
        q = self._vector(query)
        rows = self._conn.execute("SELECT memory_id,user_id,text,metadata FROM memories WHERE user_id=?", (user_id,)).fetchall()
        scored=[]
        for row in rows:
            memory=SemanticMemory(*row); v=self._vector(memory.text)
            score=sum(q.get(k,0.0)*value for k,value in v.items())
            if score > 0: scored.append((memory, score))
        return sorted(scored, key=lambda item: (-item[1], item[0].memory_id))[:limit]
