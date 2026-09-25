from pathlib import Path

from backend.tools.file_reader import FileReaderTool


def test_file_reader_reads_inside_root(tmp_path: Path) -> None:
    (tmp_path / "ok.txt").write_text("hello", encoding="utf-8")
    result = FileReaderTool(tmp_path).run({"path": "ok.txt"})
    assert result.success
    assert result.output == "hello"


def test_file_reader_rejects_path_traversal(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    result = FileReaderTool(tmp_path).run({"path": "../outside.txt"})
    assert not result.success


def test_file_reader_rejects_directory(tmp_path: Path) -> None:
    result = FileReaderTool(tmp_path).run({"path": "."})
    assert not result.success


def test_file_reader_rejects_symlink(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("secret", encoding="utf-8")
    link = tmp_path / "link.txt"
    link.symlink_to(target)
    result = FileReaderTool(tmp_path).run({"path": "link.txt"})
    assert not result.success
