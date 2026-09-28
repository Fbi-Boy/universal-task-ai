import importlib.util
from pathlib import Path


_TEST_KEY = "local-test-key-" + "x" * 40


def _load_check_local():
    spec = importlib.util.spec_from_file_location("check_local", Path("scripts/check-local.py"))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_local_launchers_validate_env_and_bind_loopback_only():
    sh = Path("scripts/run-local.sh").read_text()
    ps = Path("scripts/run-local.ps1").read_text()
    assert "scripts/check-local.py" in sh
    assert "scripts\\check-local.py" in ps
    assert "--host 127.0.0.1" in sh
    assert "--host 127.0.0.1" in ps
    assert "--env-file .env" in sh
    assert "--env-file .env" in ps
    assert "$LASTEXITCODE -ne 0" in ps
    assert "Server was not started" in ps


def test_preflight_rejects_missing_dotenv(tmp_path, monkeypatch):
    check_local = _load_check_local()
    monkeypatch.chdir(tmp_path)
    assert check_local.main() == 1


def test_preflight_requires_api_key(tmp_path, monkeypatch, capsys):
    check_local = _load_check_local()
    (tmp_path / ".env").write_text("UTA_BROWSER_ENABLED=false\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert check_local.main() == 4
    output = capsys.readouterr().out
    assert "UNIVERSAL_TASK_AI_API_KEY" in output


def test_preflight_rejects_short_api_key(tmp_path, monkeypatch):
    check_local = _load_check_local()
    (tmp_path / ".env").write_text("UNIVERSAL_TASK_AI_API_KEY=short\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert check_local.main() == 4


def test_preflight_reads_dotenv_without_printing_values(tmp_path, monkeypatch, capsys):
    check_local = _load_check_local()
    (tmp_path / ".env").write_text(
        "UNIVERSAL_TASK_AI_API_KEY=" + _TEST_KEY + "\n"
        "UTA_BROWSER_ENABLED=true\n"
        "UTA_BROWSER_ALLOWED_HOSTS=example.com\n"
        "UTA_SANDBOX_IMAGE=registry.example/uta@sha256:" + "a" * 64 + "\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    assert check_local.main() == 0
    output = capsys.readouterr().out
    assert _TEST_KEY not in output
    assert "example.com" not in output
    assert "sha256:" not in output
    assert "api_key_configured=true" in output


def test_process_environment_overrides_dotenv(tmp_path, monkeypatch):
    check_local = _load_check_local()
    (tmp_path / ".env").write_text(
        "UNIVERSAL_TASK_AI_API_KEY=" + _TEST_KEY + "\n"
        "UTA_BROWSER_ENABLED=true\nUTA_BROWSER_ALLOWED_HOSTS=example.com\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("UTA_BROWSER_ENABLED", "false")
    assert check_local.main() == 0


def test_preflight_rejects_unpinned_sandbox(tmp_path, monkeypatch):
    check_local = _load_check_local()
    (tmp_path / ".env").write_text(
        "UNIVERSAL_TASK_AI_API_KEY=" + _TEST_KEY + "\n"
        "UTA_PYTHON_SANDBOX_ENABLED=true\nUTA_SANDBOX_IMAGE=latest\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    assert check_local.main() == 3


def test_preflight_bounds_env_file(tmp_path, monkeypatch):
    check_local = _load_check_local()
    (tmp_path / ".env").write_bytes(b"#" * (64 * 1024 + 1))
    monkeypatch.chdir(tmp_path)
    assert check_local.main() == 1
