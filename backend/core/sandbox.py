from dataclasses import dataclass
import subprocess
from typing import Sequence


@dataclass(frozen=True)
class SandboxConfig:
    image: str
    timeout_seconds: int = 30
    memory: str = "256m"
    cpus: str = "0.5"
    pids_limit: int = 64

    def __post_init__(self) -> None:
        if not self.image or any(ch in self.image for ch in "\n\r"):
            raise ValueError("image must be a non-empty single-line reference")
        if self.timeout_seconds < 1 or self.timeout_seconds > 300:
            raise ValueError("timeout_seconds must be between 1 and 300")
        if self.pids_limit < 1 or self.pids_limit > 1024:
            raise ValueError("pids_limit must be between 1 and 1024")
        if not self.memory or not self.cpus:
            raise ValueError("memory and cpus are required")


class SandboxError(RuntimeError):
    pass


class DockerSandbox:
    """Execute an already-tokenized command inside a locked-down Docker container."""

    def __init__(self, config: SandboxConfig) -> None:
        self._config = config

    def build_command(self, command: Sequence[str]) -> list[str]:
        if not command or any("\x00" in part for part in command):
            raise ValueError("command must contain non-empty safe argv values")
        return [
            "docker", "run", "--rm", "--init",
            "--network=none",
            "--read-only",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges:true",
            "--pids-limit", str(self._config.pids_limit),
            "--memory", self._config.memory,
            "--cpus", self._config.cpus,
            "--tmpfs", "/tmp:rw,nosuid,nodev,noexec,size=64m",
            self._config.image,
            *command,
        ]

    def run(self, command: Sequence[str]) -> subprocess.CompletedProcess[str]:
        argv = self.build_command(command)
        try:
            return subprocess.run(
                argv,
                check=False,
                capture_output=True,
                text=True,
                timeout=self._config.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            raise SandboxError("sandbox execution timed out") from exc
        except OSError as exc:
            raise SandboxError("sandbox runtime is unavailable") from exc
