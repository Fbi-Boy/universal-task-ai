import pytest

from scripts.smoke_local import main, validate_base_url


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("http://127.0.0.1:8000", "http://127.0.0.1:8000"),
        ("http://[::1]:8000", "http://[::1]:8000"),
        ("https://127.0.0.1:8443/local/", "https://127.0.0.1:8443/local"),
    ],
)
def test_smoke_base_url_accepts_loopback_only(raw, expected):
    assert validate_base_url(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "https://attacker.example",
        "http://127.0.0.1.evil.example:8000",
        "http://127.0.0.1@attacker.example",
        "http://user:pass@127.0.0.1:8000",
        "ftp://127.0.0.1:8000",
        "http://127.0.0.1:8000/?token=secret",
        "http://127.0.0.1:8000/#fragment",
        "http://127.0.0.1:99999",
        " http://127.0.0.1:8000",
        "http://0.0.0.0:8000",
        "http://localhost:8000",
        "http://[::1%25lo0]:8000",
    ],
)
def test_smoke_base_url_rejects_untrusted_or_ambiguous_values(raw):
    with pytest.raises(ValueError):
        validate_base_url(raw)


def test_main_rejects_remote_destination_before_any_request(monkeypatch, capsys):
    import scripts.smoke_local as smoke

    monkeypatch.setenv("UTA_SMOKE_BASE_URL", "https://attacker.example")
    monkeypatch.setenv("UNIVERSAL_TASK_AI_API_KEY", "test-secret-that-must-not-leave")
    calls = []
    monkeypatch.setattr(smoke, "request", lambda *args, **kwargs: calls.append(args) or (200, {}))

    assert main() == 2
    assert calls == []
    assert "test-secret-that-must-not-leave" not in capsys.readouterr().err
