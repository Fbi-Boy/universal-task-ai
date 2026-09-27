from backend.core.execution_integrity import canonical_sha256


def test_canonical_hash_is_stable_for_mapping_order() -> None:
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})


def test_canonical_hash_changes_when_manifest_changes() -> None:
    assert canonical_sha256({"plan": "safe"}) != canonical_sha256({"plan": "tampered"})


def test_canonical_hash_is_sha256_hex() -> None:
    digest = canonical_sha256({"value": "x"})
    assert len(digest) == 64
    assert all(char in "0123456789abcdef" for char in digest)
