from pathlib import Path
from backend.local_agent.read_scope import LocalReadScope

def test_read_and_list_are_contained(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    scope = LocalReadScope(str(tmp_path))
    assert scope.read_text("a.txt") == "hello"
    assert scope.list_files() == ("a.txt",)

def test_escape_is_rejected(tmp_path: Path):
    scope = LocalReadScope(str(tmp_path))
    try:
        scope.read_text("../outside.txt")
        assert False
    except PermissionError:
        assert True
