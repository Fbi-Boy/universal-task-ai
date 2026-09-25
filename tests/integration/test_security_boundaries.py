import json

import pytest

from backend.core.egress import EgressPolicy
from backend.core.secret_provider import SecretProvider
from backend.core.network_policy import NetworkPolicy
from backend.tools.brave_search import BraveSearchProvider


@pytest.mark.integration
def test_security_boundaries_compose_without_crossing():
    secret_provider = SecretProvider(allow_environment_fallback=False)
    assert secret_provider.get("missing", required=False) is None

    egress = EgressPolicy(frozenset({"api.search.brave.com"}))
    egress.authorize("api.search.brave.com", 443)

    with pytest.raises(PermissionError):
        egress.authorize("127.0.0.1", 443)

    policy = NetworkPolicy(allowed_hosts=frozenset({"api.search.brave.com"}))
    policy.validate_url(
        "https://api.search.brave.com/res/v1/web/search?q=test",
        resolved_ips=("93.184.216.34",),
    )

    with pytest.raises(PermissionError):
        policy.validate_url(
            "https://api.search.brave.com",
            resolved_ips=("127.0.0.1",),
        )


@pytest.mark.integration
def test_external_search_provider_keeps_credential_out_of_query(monkeypatch, tmp_path):
    (tmp_path / "brave_search_api_key").write_text("integration-secret", encoding="utf-8")
    provider = BraveSearchProvider(secret_provider=SecretProvider(secret_dir=tmp_path))
    calls = []

    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *_):
            return False
        def read(self, size=-1):
            return json.dumps({"web": {"results": []}}).encode()

    def fake_urlopen(request, timeout):
        calls.append(request)
        return Response()

    monkeypatch.setattr("backend.tools.brave_search.urlopen", fake_urlopen)
    provider.search("safe query", limit=1)

    assert "integration-secret" not in calls[0].full_url
    assert calls[0].get_header("X-subscription-token") == "integration-secret"
