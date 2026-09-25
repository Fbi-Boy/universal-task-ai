from backend.tools.search import SearchResult, WebSearchTool
class Provider:
    def search(self,query,*,limit): return [SearchResult("Example","https://example.com","ok")]
def test_search_is_bounded_and_provider_driven():
    result=WebSearchTool(Provider()).run({"query":"test","limit":1})
    assert result.success and result.output[0].url=="https://example.com"
def test_search_rejects_invalid_query():
    assert not WebSearchTool(Provider()).run({"query":""}).success
