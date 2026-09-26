from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    source: str
    title: str
    url: str
    excerpt: str

@dataclass(frozen=True)
class EvidenceBundle:
    query: str
    items: tuple[Evidence,...]
    def validate(self):
        if not self.query.strip(): raise ValueError("query required")
        if not self.items: raise ValueError("at least one evidence item required")
        if any(not x.source or not x.url.startswith("https://") for x in self.items): raise ValueError("invalid evidence source")
        return self
