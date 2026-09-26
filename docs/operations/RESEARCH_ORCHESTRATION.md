# Research Orchestration

Research is modeled as evidence collection rather than unbounded text generation.

Boundary:
1. Validate query and result-count bounds.
2. Delegate to the configured search provider.
3. Require an EvidenceBundle.
4. Return source metadata for downstream review.

Untrusted web content must remain data, not instructions. Search results do not grant permissions or authorize external side effects.
