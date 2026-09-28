"""Create a secure first-run .env without overwriting existing configuration."""

from __future__ import annotations

import os
import secrets
from pathlib import Path

MAX_TEMPLATE_BYTES = 64 * 1024
API_KEY_NAME = "UNIVERSAL_TASK_AI_API_KEY"
MIN_API_KEY_LENGTH = 32


def create_local_env(project_root: Path) -> None:
    """Create .env exclusively from the checked-in template and a fresh API key.

    Existing .env files are never overwritten. On POSIX, creation requests
    owner-only permissions (0600). On Windows, normal directory ACL inheritance
    applies; users should keep the repository in a private user-owned directory.
    """
    root = project_root.resolve()
    template_path = root / ".env.example"
    target_path = root / ".env"

    if target_path.exists() or target_path.is_symlink():
        raise FileExistsError(".env already exists; it was not changed")
    if not template_path.is_file() or template_path.is_symlink():
        raise ValueError(".env.example must be a regular, non-symlink file")
    if template_path.stat().st_size > MAX_TEMPLATE_BYTES:
        raise ValueError(".env.example exceeds the setup size limit")

    template = template_path.read_text(encoding="utf-8")
    lines = template.splitlines(keepends=True)
    matches: list[int] = []
    for index, line in enumerate(lines):
        content = line.rstrip("\r\n")
        if content.startswith(f"{API_KEY_NAME}="):
            matches.append(index)
            if content.partition("=")[2].strip():
                raise ValueError("template must not contain a preset API key")

    if len(matches) != 1:
        raise ValueError("template must contain exactly one empty API key setting")

    api_key = secrets.token_urlsafe(32)
    if len(api_key) < MIN_API_KEY_LENGTH:
        raise RuntimeError("secure API key generation did not meet minimum length")

    index = matches[0]
    lines[index] = lines[index].replace(
        f"{API_KEY_NAME}=", f"{API_KEY_NAME}={api_key}", 1
    )
    content = "".join(lines)

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(target_path, flags, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())


def main() -> int:
    try:
        create_local_env(Path.cwd())
    except FileExistsError:
        print(".env already exists; no files were changed. Keep your current settings.")
        return 2
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        print(f"Local setup failed safely: {exc}")
        return 1

    print("Created .env with a fresh random API key. The key was not displayed.")
    print("Review optional capabilities before enabling them, then run scripts/check-local.py.")
    if os.name == "nt":
        print("Windows note: .env inherits the permissions of its parent directory.")
    else:
        print(".env permissions are restricted to the current user (0600).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
