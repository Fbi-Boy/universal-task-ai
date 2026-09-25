from pathlib import Path
from backend.core.semantic_memory import SQLiteSemanticMemoryStore

def test_memory_search_is_user_scoped_and_ranked(tmp_path: Path) -> None:
    store=SQLiteSemanticMemoryStore(tmp_path/"memory.db")
    store.put("u1","Python sandbox security policy")
    store.put("u1","FastAPI web interface")
    store.put("u2","Python sandbox security policy")
    results=store.search("u1","sandbox security")
    assert len(results)==1
    assert results[0][0].text.startswith("Python sandbox")
    assert results[0][1] > 0

def test_memory_limits_are_bounded(tmp_path: Path) -> None:
    store=SQLiteSemanticMemoryStore(tmp_path/"memory.db")
    try: store.search("u","q",limit=51)
    except ValueError: return
    raise AssertionError("unbounded memory search accepted")
