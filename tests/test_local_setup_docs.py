from pathlib import Path


def test_local_launchers_bind_loopback_only():
    sh = Path("scripts/run-local.sh").read_text()
    ps = Path("scripts/run-local.ps1").read_text()
    assert "--host 127.0.0.1" in sh
    assert "--host 127.0.0.1" in ps
    assert "--env-file .env" in sh
    assert "--env-file .env" in ps


def test_local_setup_keeps_high_risk_capabilities_opt_in():
    docs = Path("docs/operations/LOCAL_SETUP.md").read_text()
    assert "disabled by default" in docs
    assert "approval-gated" in docs
    assert "immutable image digest" in docs


def test_local_preflight_does_not_print_secret_values():
    script = Path("scripts/check-local.py").read_text()
    assert "API_KEY" not in script
    assert "SECRET" not in script
    assert "PASSWORD" not in script
