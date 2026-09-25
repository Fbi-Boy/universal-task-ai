from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LocalCapabilityPolicy:
    """Explicit allowlist for local-agent capabilities.

    The broker intentionally exposes read-only filesystem primitives first.
    Process execution, writes, and desktop control are separate capabilities
    and must not be implied by filesystem access.
    """

    roots: tuple[Path, ...]
    allow_read: bool = True
    max_read_bytes: int = 1_000_000

    def __post_init__(self) -> None:
        if not self.roots:
            raise ValueError("at least one local root is required")
        if self.max_read_bytes < 1 or self.max_read_bytes > 10_000_000:
            raise ValueError("max_read_bytes must be between 1 and 10000000")
        object.__setattr__(self, "roots", tuple(root.resolve() for root in self.roots))


class LocalCapabilityDenied(PermissionError):
    pass


class LocalCapabilityBroker:
    """Validate and execute the smallest safe local operations.

    Paths are resolved beneath explicitly configured roots. Symlinks are
    rejected before resolution so a symlink cannot be used to escape a root.
    No shell or arbitrary process execution is provided by this broker.
    """

    def __init__(self, policy: LocalCapabilityPolicy) -> None:
        self._policy = policy

    def _resolve_file(self, relative_path: str) -> Path:
        if not isinstance(relative_path, str) or not relative_path.strip():
            raise ValueError("path must be a non-empty string")
        if "\\x00" in relative_path:
            raise ValueError("path contains a NUL byte")

        for root in self._policy.roots:
            candidate = root / relative_path
            if candidate.is_symlink():
                raise LocalCapabilityDenied("symlink paths are not allowed")
            resolved = candidate.resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                continue
            if resolved.is_symlink():
                raise LocalCapabilityDenied("symlink targets are not allowed")
            return resolved
        raise LocalCapabilityDenied("path is outside configured local roots")

    def execute(self, operation: str, arguments: dict[str, Any]) -> Any:
        if operation != "read_text":
            raise LocalCapabilityDenied("local operation is not permitted")
        if not self._policy.allow_read:
            raise LocalCapabilityDenied("local filesystem read capability is disabled")

        candidate = self._resolve_file(arguments.get("path"))
        if not candidate.is_file():
            raise LocalCapabilityDenied("path is not an allowed regular file")
        try:
            if candidate.stat().st_size > self._policy.max_read_bytes:
                raise LocalCapabilityDenied("file exceeds local read size limit")
            return candidate.read_text(encoding="utf-8")
        except LocalCapabilityDenied:
            raise
        except (OSError, UnicodeError) as exc:
            raise LocalCapabilityDenied("file could not be read safely") from exc

    def capabilities(self) -> tuple[str, ...]:
        return ("filesystem.read_text",) if self._policy.allow_read else ()
