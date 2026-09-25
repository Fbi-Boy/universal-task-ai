from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

from backend.core.egress import EgressPolicy
from backend.core.network_policy import NetworkPolicy
from backend.core.secret_provider import SecretProvider
from backend.core.tools import Tool, ToolMetadata, ToolResult
from backend.tools.http_reader import SafeHttpReader


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class SearchProvider:
    def search(self, query: str, *, limit: int = 10) -> list[SearchResult]:
        raise NotImplementedError


class BraveSearchProvider(SearchProvider):
    """Concrete Brave Search adapter behind the hardened HTTP boundary."""

    def __init__(self, api_key: str, reader: SafeHttpReader) -> None:
        if not api_key:
            raise ValueError("Brave search API key is required")
        self._api_key = api_key
        self._reader = reader

    @classmethod
    def from_secrets(cls, *, secret_provider=None, reader=None) -> "BraveSearchProvider":
        secrets = secret_provider or SecretProvider()
        api_key = secrets.get("brave_search_api_key", env_name="BRAVE_SEARCH_API_KEY")
        configured_reader = reader or SafeHttpReader(
            NetworkPolicy(
                allowed_hosts=frozenset({"api.search.brave.com"}),
                max_response_bytes=2 * 1024 * 1024,
                timeout_seconds=10,
                max_redirects=2,
            ),
            egress=EgressPolicy(
                allowed_hosts=frozenset({"api.search.brave.com"}),
                allowed_ports=frozenset({443}),
            ),
        )
        return cls(api_key, configured_reader)

    def search(self, query: str, *, limit: int = 10) -> list[SearchResult]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be non-empty")
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
            raise ValueError("limit must be between 1 and 20")
        url = f"https://api.search.brave.com/res/v1/web/search?q={quote(query, safe='')}&count={limit}"
        response = self._reader.read_with_headers(
            url,
            headers={"Accept": "application/json", "X-Subscription-Token": self._api_key},
        )
        if response["status"] != 200:
            raise RuntimeError("Brave search request failed")
        rows = response["json"].get("web", {}).get("results", [])
        if not isinstance(rows, list):
            raise RuntimeError("Brave search response is malformed")
        output = []
        for row in rows[:limit]:
            if not isinstance(row, dict):
                continue
            title, result_url = row.get("title"), row.get("url")
            if not isinstance(title, str) or not isinstance(result_url, str):
                continue
            if not result_url.startswith(("https://", "http://")):
                continue
            output.append(SearchResult(title[:500], result_url[:2000], str(row.get("description", ""))[:2000]))
        return output


class WebSearchTool(Tool):
    metadata = ToolMetadata(
        name="web_search",
        description="Search the web through an explicitly configured provider",
        risk_level="medium",
        requires_network=True,
        requires_approval=True,
    )

    def __init__(self, provider: SearchProvider, *, max_query_length: int = 500, max_results: int = 10) -> None:
        if max_query_length < 1 or max_query_length > 2_000 or max_results < 1 or max_results > 50:
            raise ValueError("invalid search bounds")
        self._provider, self._max_query_length, self._max_results = provider, max_query_length, max_results

    def run(self, arguments):
        query = arguments.get("query")
        limit = arguments.get("limit", self._max_results)
        if not isinstance(query, str) or not query.strip() or len(query) > self._max_query_length:
            return ToolResult(success=False, error="invalid query")
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1 or limit > self._max_results:
            return ToolResult(success=False, error="invalid result limit")
        try:
            return ToolResult(success=True, output=self._provider.search(query, limit=limit))
        except Exception:
            return ToolResult(success=False, error="search provider failed")
