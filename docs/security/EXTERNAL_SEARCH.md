# External search adapter

Universal Task AI now includes a concrete Brave Search adapter at `backend/tools/brave_search.py`.

Security properties:
- fixed HTTPS provider host and path; user input only becomes a URL-encoded query
- egress policy authorizes the fixed host on port 443
- API credential comes only from `BRAVE_SEARCH_API_KEY`, never tool arguments
- bounded query/result sizes
- bounded response body
- explicit timeout
- provider failures stay behind the existing `WebSearchTool` sanitized error boundary

This adapter is intentionally separate from generic HTTP reading so arbitrary task input cannot select an external host.
