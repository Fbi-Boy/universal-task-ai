import os
from pathlib import Path

_ALLOWED_KEYS = {
    "UNIVERSAL_TASK_AI_API_KEY",
    "UTA_BROWSER_ENABLED",
    "UTA_BROWSER_ALLOWED_HOSTS",
    "UTA_LOCAL_ROOTS",
    "UTA_PYTHON_SANDBOX_ENABLED",
    "UTA_SANDBOX_IMAGE",
}
_MAX_ENV_FILE_BYTES = 64 * 1024
_MIN_API_KEY_LENGTH = 32
_PLACEHOLDER_KEYS = {"changeme", "change-me", "your-api-key", "replace-me"}


def _load_env_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(".env is missing")
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
    try:
        env_file = _load_env_file(Path(".env"))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Invalid .env: {exc}")
        return 1

    api_key = _setting(env_file, "UNIVERSAL_TASK_AI_API_KEY").strip()
    if (
        len(api_key) < _MIN_API_KEY_LENGTH
        or api_key.lower() in _PLACEHOLDER_KEYS
    ):
        print(
            "UNIVERSAL_TASK_AI_API_KEY must be configured with a random value "
            "of at least 32 characters; generate one with Python secrets."
        )
        return 4

    browser = _setting(env_file, "UTA_BROWSER_ENABLED", "false").lower() == "true"
    sandbox = _setting(env_file, "UTA_PYTHON_SANDBOX_ENABLED", "false").lower() == "true"
    roots = bool(_setting(env_file, "UTA_LOCAL_ROOTS").strip())

    print("api_key_configured=true")
    print(f"browser_enabled={browser}")
    print(f"local_roots_configured={roots}")
    print(f"python_sandbox_enabled={sandbox}")

    if browser and not _setting(env_file, "UTA_BROWSER_ALLOWED_HOSTS").strip():
        print("Browser is enabled but UTA_BROWSER_ALLOWED_HOSTS is empty.")
        return 2
    sandbox_image = _setting(env_file, "UTA_SANDBOX_IMAGE").strip()
    if sandbox and "@sha256:" not in sandbox_image:
        print("Python sandbox requires an immutable sha256 image reference.")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
