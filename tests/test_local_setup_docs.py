from pathlib import Path


def test_local_launchers_bind_loopback_only_and_fail_closed():
    sh = Path("scripts/run-local.sh").read_text()
    ps = Path("scripts/run-local.ps1").read_text()
    assert "--host 127.0.0.1" in sh
    assert "--host 127.0.0.1" in ps
    assert "--env-file .env" in sh
    assert "--env-file .env" in ps
    assert "$LASTEXITCODE -ne 0" in ps
    assert "Server was not started" in ps


def test_local_setup_keeps_high_risk_capabilities_opt_in():
    docs = Path("docs/operations/LOCAL_SETUP.md").read_text()
    assert "disabled by default" in docs
    assert "approval-gated" in docs
    assert "immutable image digest" in docs
    assert "UNIVERSAL_TASK_AI_API_KEY" in docs


def test_local_preflight_does_not_print_secret_values():
    script = Path("scripts/check-local.py").read_text()
    assert "UNIVERSAL_TASK_AI_API_KEY" in script
    assert "print(api_key)" not in script
    assert "print(_setting" not in script
    assert "SECRET" not in script
    assert "PASSWORD" not in script


def test_quickstart_documents_secure_key_generation_and_launch():
    docs = Path("docs/LOCAL_SETUP.md").read_text()
    assert "secrets.token_urlsafe(32)" in docs
    assert "127.0.0.1" in docs
    assert "server does not start" in docs
