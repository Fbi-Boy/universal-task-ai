from backend.core.release import build_sha, build_version


def test_build_identity_defaults(monkeypatch):
    monkeypatch.delenv("UTA_BUILD_VERSION", raising=False)
    monkeypatch.delenv("UTA_BUILD_SHA", raising=False)
    assert build_version() == "0.1.0"
    assert build_sha() == "unknown"


def test_build_identity_is_bounded_to_configured_values(monkeypatch):
    monkeypatch.setenv("UTA_BUILD_VERSION", "0.1.0-test")
    monkeypatch.setenv("UTA_BUILD_SHA", "abc123")
    assert build_version() == "0.1.0-test"
    assert build_sha() == "abc123"
