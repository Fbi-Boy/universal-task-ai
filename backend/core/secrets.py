from collections.abc import Mapping


_BLOCKED_KEYS = frozenset({"password", "passwd", "token", "secret", "api_key", "authorization", "cookie"})


def redact_metadata(metadata: Mapping[str, object]) -> dict[str, object]:
    return {key: ("[REDACTED]" if key.lower() in _BLOCKED_KEYS else value) for key, value in metadata.items()}
