from backend.core.brave_research_provider import BraveResearchProvider

class RuntimeResearchService:
    def __init__(self, brave_provider):
        self.provider=BraveResearchProvider(brave_provider)

    def search(self, request):
        return self.provider.search(request)
