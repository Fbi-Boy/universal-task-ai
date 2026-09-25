from backend.tools.search import BraveSearchProvider, SearchResult, WebSearchTool


class Provider:
    def search(self, query, *, limit):
        return [SearchResult("Example", "https://example.com", "ok")]


class Reader:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def read_with_headers(self, url, *, headers):
        self.calls.append((url, headers))
        return {"status": 200, "json": self.payload}


def test_search_is_bounded_and_provider_driven():
    result = WebSearchTool(Provider()).run({"query": "test", "limit": 1})
    assert result.success and result.output[0].url == "https://example.com"


def test_search_rejects_invalid_query():
    assert not WebSearchTool(Provider()).run({"query": ""}).success


def test_brave_provider_maps_results_and_keeps_credential_out_of_url():
    reader = Reader({"web": {"results": [
        {"title": "A", "url": "https://a.example", "description": "first"},
        {"title": "B", "url": "https://b.example", "description": "second"},
    ]}})
    provider = BraveSearchProvider("secret", reader)
    results = provider.search("hello world", limit=1)
    assert [r.title for r in results] == ["A"]
    assert "secret" not in reader.calls[0][0]
    assert reader.calls[0][1]["X-Subscription-Token"] == "secret"


def test_brave_provider_rejects_invalid_limit():
    provider = BraveSearchProvider("secret", Reader({"web": {"results": []}}))
    try:
        provider.search("hello", limit=0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected invalid limit")


def test_brave_provider_ignores_malformed_rows():
    reader = Reader({"web": {"results": ["bad", {"title": "ok", "url": "https://ok.example"}]}})
    provider = BraveSearchProvider("secret", reader)
    assert [r.title for r in provider.search("hello")] == ["ok"]
