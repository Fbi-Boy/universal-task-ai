import json
import os
from dataclasses import dataclass
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from backend.core.egress import EgressPolicy
from backend.tools.search import SearchResult


@dataclass(frozen=True)
class BraveSearchProvider:
    """Bounded adapter for the Brave Search HTTP API.

    The API host/path are fixed so a task cannot turn the provider into a
    generic HTTP client. Credentials are read from the process environment
    and are never accepted as tool arguments.
    """

    api_key_env: str = "BRAVE_SEARCH_API_KEY"
    max_response_bytes: int = 1_000_000
    timeout_seconds: float = 8.0
    egress_policy: EgressPolicy = EgressPolicy(frozenset({"api.search.brave.com"}))

    def search(self, query: str, *, limit: int = 10) -> list[SearchResult]:
        if not isinstance(query, str) or not query.strip() or len(query) > 500:
            raise ValueError("invalid query")
        if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
            raise ValueError("invalid result limit")

        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise RuntimeError("search provider is not configured")

        host = "api.search.brave.com"
        self.egress_policy.authorize(host, 443)
        url = (
            "https://api.search.brave.com/res/v1/web/search"
            f"?q={quote_plus(query)}&count={limit}"
        )
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "X-Subscription-Token": api_key,
                "User-Agent": "universal-task-ai/1",
            },
            method="GET",
        )
        with urlopen(request, timeout=self.timeout_seconds) as response:
            raw = response.read(self.max_response_bytes + 1)
        if len(raw) > self.max_response_bytes:
            raise RuntimeError("search response exceeded size limit")
        payload = json.loads(raw)
        results = payload.get("web", {}).get("results", [])
        if not isinstance(results, list):
            raise RuntimeError("invalid search response")

        output: list[SearchResult] = []
        for item in results[:limit]:
            if not isinstance(item, dict):
                continue
            title, url_value = item.get("title"), item.get("url")
            snippet = item.get("description", "")
            if isinstance(title, str) and isinstance(url_value, str):
                output.append(SearchResult(title=title[:500], url=url_value[:2_000], snippet=str(snippet)[:2_000]))
        return output
