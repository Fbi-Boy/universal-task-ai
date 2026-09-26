from unittest.mock import patch

import pytest

from backend.core.sandbox import DockerSandbox, SandboxConfig, SandboxError


def test_build_command_has_isolation_and_resource_limits() -> None:
    cmd = DockerSandbox(SandboxConfig("python:3.11@sha256:" + "a" * 64, timeout_seconds=10)).build_command(["python", "-c", "print(1)"])
    assert cmd[:3] == ["docker", "run", "--rm"]
    for flag in ("--network=none", "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges:true"):
        assert flag in cmd
    assert "--memory" in cmd and "256m" in cmd
    assert "--cpus" in cmd and "0.5" in cmd
    assert "--pids-limit" in cmd and "64" in cmd


def test_config_bounds() -> None:
    with pytest.raises(ValueError):
        SandboxConfig("image@sha256:" + "a" * 64, timeout_seconds=0)
    with pytest.raises(ValueError):
        SandboxConfig("image@sha256:" + "a" * 64, pids_limit=0)
    with pytest.raises(ValueError):
        SandboxConfig("bad\nimage")


def test_run_uses_tokenized_argv_and_timeout() -> None:
    completed = type("Completed", (), {"returncode": 0})()
    with patch("backend.core.sandbox.subprocess.run", return_value=completed) as run:
        result = DockerSandbox(SandboxConfig("image@sha256:" + "a" * 64, timeout_seconds=7)).run(["python", "-c", "print(1)"])
    assert result is completed
    kwargs = run.call_args.kwargs
    assert kwargs["timeout"] == 7
    assert kwargs["shell"] if "shell" in kwargs else False is False
    assert run.call_args.args[0][-4:] == ["image@sha256:" + "a" * 64, "python", "-c", "print(1)"]


def test_runtime_errors_are_wrapped() -> None:
    with patch("backend.core.sandbox.subprocess.run", side_effect=OSError("missing docker")):
        with pytest.raises(SandboxError):
            DockerSandbox(SandboxConfig("image@sha256:" + "a" * 64)).run(["python", "-c", "pass"])
