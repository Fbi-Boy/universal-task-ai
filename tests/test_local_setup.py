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


def test_setup_generator_creates_key_without_printing_it(tmp_path, monkeypatch, capsys):
    import os
    from scripts.setup_local import API_KEY_NAME, main

    root = tmp_path / "project"
    root.mkdir()
    (root / ".env.example").write_text(
        f"# template\n{API_KEY_NAME}=\nUTA_BROWSER_ENABLED=false\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(root)
    assert main() == 0
    env_text = (root / ".env").read_text(encoding="utf-8")
    key = next(line.partition("=")[2] for line in env_text.splitlines()
               if line.startswith(f"{API_KEY_NAME}="))
    assert len(key) >= 32
    assert "UTA_BROWSER_ENABLED=false" in env_text
    assert key not in capsys.readouterr().out
    if os.name == "posix":
        assert (root / ".env").stat().st_mode & 0o777 == 0o600


def test_setup_generator_never_overwrites_existing_env(tmp_path):
    import pytest
    from scripts.setup_local import create_local_env

    root = tmp_path / "project"
    root.mkdir()
    (root / ".env.example").write_text("UNIVERSAL_TASK_AI_API_KEY=\n", encoding="utf-8")
    sentinel = "UNIVERSAL_TASK_AI_API_KEY=existing-secret-value\n"
    (root / ".env").write_text(sentinel, encoding="utf-8")
    with pytest.raises(FileExistsError):
        create_local_env(root)
    assert (root / ".env").read_text(encoding="utf-8") == sentinel


def test_setup_generator_rejects_unsafe_templates(tmp_path):
    import pytest
    from scripts.setup_local import create_local_env

    root = tmp_path / "project"
    root.mkdir()
    for template in (
        "UTA_BROWSER_ENABLED=false\n",
        "UNIVERSAL_TASK_AI_API_KEY=\nUNIVERSAL_TASK_AI_API_KEY=\n",
        "UNIVERSAL_TASK_AI_API_KEY=accidental-secret\n",
        "UNIVERSAL_TASK_AI_API_KEY=\n  UNIVERSAL_TASK_AI_API_KEY=hidden-preset-secret\n",
    ):
        (root / ".env.example").write_text(template, encoding="utf-8")
        with pytest.raises(ValueError):
            create_local_env(root)
        assert not (root / ".env").exists()


def test_setup_generator_rejects_symlink_template(tmp_path):
    import pytest
    from scripts.setup_local import create_local_env

    root = tmp_path / "project"
    root.mkdir()
    external = tmp_path / "external-template"
    external.write_text("UNIVERSAL_TASK_AI_API_KEY=\n", encoding="utf-8")
    (root / ".env.example").symlink_to(external)
    with pytest.raises(ValueError):
        create_local_env(root)
    assert not (root / ".env").exists()
