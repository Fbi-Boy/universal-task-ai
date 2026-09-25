from pathlib import Path

import pytest

from backend.local_agent.broker import (
    LocalCapabilityBroker,
    LocalCapabilityDenied,
    LocalCapabilityPolicy,
)


def test_read_text_is_limited_to_configured_root(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    (root / "note.txt").write_text("hello", encoding="utf-8")

    broker = LocalCapabilityBroker(LocalCapabilityPolicy((root,)))

    assert broker.execute("read_text", {"path": "note.txt"}) == "hello"


def test_parent_escape_is_denied(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    (tmp_path / "secret.txt").write_text("secret", encoding="utf-8")
    broker = LocalCapabilityBroker(LocalCapabilityPolicy((root,)))

    with pytest.raises(LocalCapabilityDenied):
        broker.execute("read_text", {"path": "../secret.txt"})


def test_symlink_escape_is_denied(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    secret = tmp_path / "secret.txt"
    secret.write_text("secret", encoding="utf-8")
    (root / "link.txt").symlink_to(secret)
    broker = LocalCapabilityBroker(LocalCapabilityPolicy((root,)))

    with pytest.raises(LocalCapabilityDenied):
        broker.execute("read_text", {"path": "link.txt"})


def test_arbitrary_operations_are_denied(tmp_path: Path) -> None:
    broker = LocalCapabilityBroker(LocalCapabilityPolicy((tmp_path,)))

    with pytest.raises(LocalCapabilityDenied):
        broker.execute("shell", {"command": "whoami"})


def test_size_limit_is_enforced(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    (root / "large.txt").write_text("12345", encoding="utf-8")
    broker = LocalCapabilityBroker(LocalCapabilityPolicy((root,), max_read_bytes=4))

    with pytest.raises(LocalCapabilityDenied):
        broker.execute("read_text", {"path": "large.txt"})
