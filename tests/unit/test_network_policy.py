import pytest

from backend.core.network_policy import NetworkPolicy


def test_https_public_host_is_allowed() -> None:
    NetworkPolicy().validate_url("https://example.com", resolved_ips=("93.184.216.34",))


def test_http_is_denied_by_default() -> None:
    with pytest.raises(PermissionError):
        NetworkPolicy().validate_url("http://example.com")


def test_local_and_private_targets_are_denied() -> None:
    policy = NetworkPolicy()
    for url in ("https://localhost", "https://127.0.0.1", "https://10.0.0.1"):
        with pytest.raises(PermissionError):
            policy.validate_url(url)


def test_dns_rebinding_to_private_address_is_denied() -> None:
    with pytest.raises(PermissionError):
        NetworkPolicy().validate_url("https://example.com", resolved_ips=("192.168.1.5",))


def test_credentials_and_non_allowlisted_host_are_denied() -> None:
    policy = NetworkPolicy(allowed_hosts=frozenset({"api.example.com"}))
    with pytest.raises(PermissionError):
        policy.validate_url("https://user:pass@api.example.com")
    with pytest.raises(PermissionError):
        policy.validate_url("https://other.example.com")


def test_limits_are_bounded() -> None:
    with pytest.raises(ValueError):
        NetworkPolicy(timeout_seconds=121)
    with pytest.raises(ValueError):
        NetworkPolicy(max_response_bytes=0)
    with pytest.raises(ValueError):
        NetworkPolicy(max_redirects=11)
