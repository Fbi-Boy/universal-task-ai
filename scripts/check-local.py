import os
from pathlib import Path

_ALLOWED_KEYS = {
    "UTA_BROWSER_ENABLED",
    "UTA_BROWSER_ALLOWED_HOSTS",
    "UTA_LOCAL_ROOTS",
    "UTA_PYTHON_SANDBOX_ENABLED",
    "UTA_SANDBOX_IMAGE",
}
_MAX_ENV_FILE_BYTES = 64 * 1024


def _load_env_file(path: Path) -> dict[str, str]:
    if path.stat().st_size > _MAX_ENV_FILE_BYTES:
        raise ValueError(".env exceeds the preflight size limit")
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, value = line.partition("=")
        if not separator or key not in _ALLOWED_KEYS:
            continue
        values[key] = value.strip().strip("'").strip('"')
    return values


def _setting(env_file: dict[str, str], key: str, default: str = "") -> str:
    return os.environ.get(key, env_file.get(key, default))


def main() -> int:
    env_path = Path(".env")
    if not env_path.is_file():
        print("Missing .env. Copy .env.example to .env first.")
        return 1

    try:
        env_file = _load_env_file(env_path)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Invalid .env: {exc}")
        return 1

    browser = _setting(env_file, "UTA_BROWSER_ENABLED", "false").lower() == "true"
    sandbox = _setting(env_file, "UTA_PYTHON_SANDBOX_ENABLED", "false").lower() == "true"
    roots = bool(_setting(env_file, "UTA_LOCAL_ROOTS").strip())
    print(f"browser_enabled={browser}")
    print(f"local_roots_configured={roots}")
    print(f"python_sandbox_enabled={sandbox}")
    if browser and not _setting(env_file, "UTA_BROWSER_ALLOWED_HOSTS").strip():
        print("Browser is enabled but UTA_BROWSER_ALLOWED_HOSTS is empty.")
        return 2
    if sandbox and "@sha256:" not in _setting(env_file, "UTA_SANDBOX_IMAGE"):
        print("Python sandbox requires an immutable sha256 image reference.")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
