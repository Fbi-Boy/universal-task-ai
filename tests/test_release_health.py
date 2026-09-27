from backend.api.main import health


def test_health_exposes_non_secret_build_identity(monkeypatch):
    monkeypatch.setenv("UTA_BUILD_VERSION", "0.1.0-test")
    monkeypatch.setenv("UTA_BUILD_SHA", "abc123")
    assert health() == {
        "status": "ok",
        "version": "0.1.0-test",
        "build_sha": "abc123",
    }
