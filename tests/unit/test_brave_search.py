import json

import pytest

from backend.core.egress import EgressPolicy
from backend.tools.brave_search import BraveSearchProvider


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, size=-1):
        if size >= 0:
            return self.payload[:size]
        return self.payload


def test_brave_search_provider_parses_bounded_results(monkeypatch):
    calls = []

    def fake_urlopen(request, timeout):
        calls.append((request.full_url, request.headers, timeout))
        return FakeResponse(json.dumps({"web": {"results": [
            {"title": "A", "url": "https://example.com/a", "description": "alpha"},
            {"title": "B", "url": "https://example.com/b", "description": "beta"},
        ]}}).encode())

    monkeypatch.setenv("BRAVE_SEARCH_API_KEY", "test-secret")
    monkeypatch.setattr("backend.tools.brave_search.urlopen", fake_urlopen)
    provider = BraveSearchProvider(egress_policy=EgressPolicy(frozenset({"api.search.brave.com"})))
    results = provider.search("hello world", limit=2)

    assert [r.title for r in results] == ["A", "B"]
    assert "test-secret" in calls[0][1]["X-subscription-token"]
    assert "hello+world" in calls[0][0]


def test_brave_search_requires_secret(monkeypatch):
    monkeypatch.delenv("BRAVE_SEARCH_API_KEY", raising=False)
    provider = BraveSearchProvider()
    with pytest.raises(RuntimeError, match="not configured"):
        provider.search("hello")


def test_brave_search_rejects_unbounded_response(monkeypatch):
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY", "test")
    monkeypatch.setattr(
        "backend.tools.brave_search.urlopen",
        lambda request, timeout: FakeResponse(b"x" * 101),
    )
    provider = BraveSearchProvider(max_response_bytes=100)
    with pytest.raises(RuntimeError, match="size limit"):
        provider.search("hello")


def test_brave_search_can_use_mounted_secret(monkeypatch, tmp_path):
    from backend.core.secret_provider import SecretProvider

    (tmp_path / "brave_search_api_key").write_text("mounted-secret", encoding="utf-8")
    monkeypatch.delenv("BRAVE_SEARCH_API_KEY", raising=False)
    provider = BraveSearchProvider(secret_provider=SecretProvider(secret_dir=tmp_path))
    assert provider.secret_provider.get("brave_search_api_key", required=False) == "mounted-secret"
