from dataclasses import dataclass
from typing import Protocol

from backend.core.tools import Tool, ToolMetadata, ToolResult

@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str = ""

class SearchProvider(Protocol):
    def search(self, query: str, *, limit: int = 10) -> list[SearchResult]: ...

class WebSearchTool(Tool):
    metadata = ToolMetadata(name="web_search", description="Search the web through an explicitly configured provider", risk_level="medium", requires_network=True, requires_approval=True)
    def __init__(self, provider: SearchProvider, *, max_query_length: int = 500, max_results: int = 10) -> None:
        if max_query_length < 1 or max_query_length > 2_000 or max_results < 1 or max_results > 50: raise ValueError("invalid search bounds")
        self._provider, self._max_query_length, self._max_results = provider, max_query_length, max_results
    def run(self, arguments):
        query=arguments.get("query")
        limit=arguments.get("limit", self._max_results)
        if not isinstance(query,str) or not query.strip() or len(query)>self._max_query_length: return ToolResult(success=False,error="invalid query")
        if not isinstance(limit,int) or isinstance(limit,bool) or limit<1 or limit>self._max_results: return ToolResult(success=False,error="invalid result limit")
        try: return ToolResult(success=True,output=self._provider.search(query,limit=limit))
        except Exception: return ToolResult(success=False,error="search provider failed")
