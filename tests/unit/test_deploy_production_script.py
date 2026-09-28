import os
import subprocess
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "deploy-production.sh"
IMAGE_DIGEST = "sha256:" + "a" * 64
VALID_IMAGE = f"ghcr.io/fbi-boy/universal-task-ai@{IMAGE_DIGEST}"


@pytest.fixture
def fake_ssh(tmp_path: Path) -> tuple[dict[str, str], Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    ssh = bin_dir / "ssh"
    ssh.write_text(
        '#!/bin/sh\nprintf "%s\\n" "$*" >> "$SSH_CAPTURE"\n',
        encoding="utf-8",
    )
    ssh.chmod(0o755)
    capture = tmp_path / "ssh-calls.txt"
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}{os.pathsep}{env.get('PATH', '')}",
            "SSH_CAPTURE": str(capture),
            "IMAGE": VALID_IMAGE,
            "DEPLOY_HOST": "deploy.example.test",
            "DEPLOY_USER": "deploy",
            "DEPLOY_PATH": "/srv/universal-task-ai",
        }
    )
    return env, capture


def _run(env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(SCRIPT)],
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )


def test_deploy_script_uses_digest_and_shell_safe_remote_command(fake_ssh) -> None:
    env, capture = fake_ssh
    result = _run(env)
    assert result.returncode == 0, result.stderr
    calls = capture.read_text(encoding="utf-8").splitlines()
    assert len(calls) == 2
    assert VALID_IMAGE in calls[0]
    assert "docker compose" in calls[0]
    assert "/srv/universal-task-ai" in calls[0]


def test_deploy_script_rejects_mutable_tag_before_ssh(fake_ssh) -> None:
    env, capture = fake_ssh
    env["IMAGE"] = "ghcr.io/fbi-boy/universal-task-ai:latest"
    result = _run(env)
    assert result.returncode != 0
    assert "sha256 digest" in result.stderr
    assert not capture.exists()


@pytest.mark.parametrize(
    "unsafe_path",
    [
        "/srv/app'; touch /tmp/uta-injected; echo '",
        "/srv/../etc",
        "relative/path",
    ],
)
def test_deploy_script_rejects_unsafe_paths_before_ssh(fake_ssh, unsafe_path: str) -> None:
    env, capture = fake_ssh
    env["DEPLOY_PATH"] = unsafe_path
    result = _run(env)
    assert result.returncode != 0
    assert "DEPLOY_PATH" in result.stderr
    assert not capture.exists()


def test_deploy_script_rejects_invalid_image_digest_before_ssh(fake_ssh) -> None:
    env, capture = fake_ssh
    env["IMAGE"] = "ghcr.io/fbi-boy/universal-task-ai@sha256:bad"
    result = _run(env)
    assert result.returncode != 0
    assert not capture.exists()
