from dataclasses import dataclass
from ipaddress import ip_address
from urllib.parse import urlparse


_BLOCKED_HOSTNAMES = frozenset({"localhost", "localhost.localdomain"})
_BLOCKED_SUFFIXES = (".localhost", ".local", ".internal", ".home.arpa")


@dataclass(frozen=True)
class NetworkPolicy:
    """Pure network policy checks; callers must revalidate every redirect."""

    allowed_hosts: frozenset[str] = frozenset()
    allow_http: bool = False
    max_response_bytes: int = 10 * 1024 * 1024
    timeout_seconds: float = 10.0
    max_redirects: int = 5

    def __post_init__(self) -> None:
        if self.max_response_bytes < 1 or self.max_response_bytes > 100 * 1024 * 1024:
            raise ValueError("max_response_bytes must be between 1 and 100 MiB")
        if self.timeout_seconds <= 0 or self.timeout_seconds > 120:
            raise ValueError("timeout_seconds must be > 0 and <= 120")
        if self.max_redirects < 0 or self.max_redirects > 10:
            raise ValueError("max_redirects must be between 0 and 10")

    def validate_url(self, url: str, *, resolved_ips: tuple[str, ...] = ()) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in {"https", "http" if self.allow_http else "https"}:
            raise PermissionError("URL scheme is not permitted")
        if parsed.username is not None or parsed.password is not None:
            raise PermissionError("URL credentials are not permitted")
        host = parsed.hostname
        if not host:
            raise PermissionError("URL hostname is required")
        normalized = host.rstrip(".").lower()
        if normalized in _BLOCKED_HOSTNAMES or normalized.endswith(_BLOCKED_SUFFIXES):
            raise PermissionError("local or internal hostname is not permitted")
        try:
            literal = ip_address(normalized)
        except ValueError:
            literal = None
        if literal is not None:
            self._validate_public_ip(str(literal))
        elif self.allowed_hosts and normalized not in {h.rstrip(".").lower() for h in self.allowed_hosts}:
            raise PermissionError("hostname is not on the allowlist")
        for resolved in resolved_ips:
            self._validate_public_ip(resolved)

    @staticmethod
    def _validate_public_ip(value: str) -> None:
        try:
            address = ip_address(value)
        except ValueError as exc:
            raise PermissionError("resolved address is invalid") from exc
        if (
            address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_multicast
            or address.is_unspecified
            or address.is_reserved
        ):
            raise PermissionError("private, local, reserved, or special-use address is not permitted")
