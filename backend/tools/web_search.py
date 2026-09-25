from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str


class WebSearchProvider(Protocol):
    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        ...


def validate_search_query(query: str, *, max_length: int = 2_000) -> str:
    value = query.strip()
    if not value:
        raise ValueError("query must not be empty")
    if len(value) > max_length:
        raise ValueError("query is too long")
    return value
