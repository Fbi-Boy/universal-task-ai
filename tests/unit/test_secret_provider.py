import pytest
from backend.core.secret_provider import SecretNotConfigured, SecretProvider


def test_secret_provider_reads_mounted_secret_before_environment(tmp_path, monkeypatch):
    (tmp_path / "api_key").write_text("file-secret\n", encoding="utf-8")
    monkeypatch.setenv("TEST_SECRET", "env-secret")
    provider = SecretProvider(secret_dir=tmp_path)
    assert provider.get("api_key", env_name="TEST_SECRET") == "file-secret"


def test_secret_provider_uses_explicit_env_fallback(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_SECRET", "env-secret")
    provider = SecretProvider(secret_dir=tmp_path)
    assert provider.get("api_key", env_name="TEST_SECRET") == "env-secret"


def test_secret_provider_does_not_fallback_when_disabled(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_SECRET", "env-secret")
    provider = SecretProvider(secret_dir=tmp_path, allow_environment_fallback=False)
    with pytest.raises(SecretNotConfigured):
        provider.get("api_key", env_name="TEST_SECRET")


@pytest.mark.parametrize("name", ["../x", "/tmp/x", "x/y", "x\\y", ".", ".."])
def test_secret_name_cannot_escape_secret_directory(tmp_path, name):
    with pytest.raises(ValueError):
        SecretProvider(secret_dir=tmp_path).get(name)


def test_missing_optional_secret_returns_none(tmp_path):
    assert SecretProvider(secret_dir=tmp_path).get("missing", required=False) is None
