from pathlib import Path

import pytest

from backend.core.artifacts import ArtifactStore


def test_store_round_trip_and_hash(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path / "artifacts")
    artifact = store.put("result.txt", b"hello")
    assert artifact.size == 5
    assert len(artifact.sha256) == 64
    assert store.get(artifact) == b"hello"


def test_name_and_size_policy(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path / "artifacts", max_size_bytes=4)
    with pytest.raises(ValueError):
        store.put("../escape.txt", b"x")
    with pytest.raises(ValueError):
        store.put("large.txt", b"12345")


def test_tampering_is_detected(tmp_path: Path) -> None:
    store = ArtifactStore(tmp_path / "artifacts")
    artifact = store.put("result.txt", b"hello")
    artifact.path.write_bytes(b"changed")
    with pytest.raises(ValueError):
        store.get(artifact)
