# Universal Task AI — Instructions for AI Agents

This file is the repository-level entry point for every AI coding, design, research, QA, and release agent working on this repository. Read it before acting.

## Mandatory reading order

1. [Agent Operating System & Product Governance](docs/agent-system/AGENT_OPERATING_SYSTEM.md) — source of truth for agent hierarchy, gates, roles, prompts, standards, sprint order, acceptance scenarios, and Definition of Done.
2. [Product & Engineering Blueprint](docs/agent-system/PRODUCT_BLUEPRINT.md) — product scope, architecture, data model, API contracts, delivery roadmap, and end-to-end flows.
3. [Design Reference Board](docs/agent-system/DESIGN_REFERENCE_BOARD.html) — open in a browser to inspect visual screenshots and original sources.
4. [Design Reference Matrix](docs/agent-system/DESIGN_REFERENCE_MATRIX.md) — mapping of product areas to visual inspiration, official behavior docs, implementation references, and design direction.
5. Inspect current repository code, branch, open PRs, workflows, and tests. Historical documentation must never override current source or CI evidence.

## Non-negotiable rules

- A0 Chief Architect is the single coordinator for project scope, shared contracts, dependencies, ticket assignment, and integration decisions. Agents do not independently redefine architecture.
- No production-facing page may be implemented before the page brief, screenshot-based reference board, design-system mapping, and owner design approval are recorded. Visual search alone is not approval.
- Research before implementation. Use real screenshots/images from credible visual sources such as Dribbble, Behance, Pinterest, real product UI, and official docs as relevant. Link every source, explain what to adopt/reject, and distinguish visual inspiration from behavioral/technical evidence. Never copy proprietary assets into the product without rights.
- Maintain one coherent design system: shared tokens, typography, spacing, responsive behavior, icon family, components, states, and terminology across all routes and roles. No unrelated page-by-page designs or generic AI-generated layouts.
- Never fabricate product metrics, task activity, connected integrations, status, outputs, or test results. Demo data must be visibly labeled and test-only.
- Inspect existing implementation and open PRs before changing code. Prefer small, auditable vertical slices over rewrites or mega-PRs.
- Preserve least privilege, authorization, tenant isolation, secret protection, auditability, idempotency, and human approvals for risky side effects. Model output may not grant itself tools or permissions.
- Campus connections must use authorized APIs/integrations and respect consent. Never spoof attendance, impersonate students, or silently perform official academic actions.
- Every task must have an owner, scope in/out, allowed paths, dependencies, acceptance criteria, failure/security cases, test plan, and documentation expectations.
- Done requires evidence: exact commands run, results, PR/commit links, screenshots for UI work, known limitations, and a reviewer. Mark unrun checks as NOT RUN.
- Do not merge, deploy, change secrets/permissions, or perform destructive operations without the relevant approval. Do not claim production readiness until release, rollback, health, persistence, and security evidence has been checked.

## Coordination protocol

Every agent reports: ticket ID, branch/PR, changed paths, shared contracts changed, tests run and results, screenshot/reference comparison where relevant, security/failure cases considered, risks/blockers, and remaining work. A12 independently reviews security, correctness, accessibility, and reliability; A0 confirms integration. Owner approves product direction and visual direction. Review and CI must be against the latest PR head.

If documentation and code disagree, inspect current source and tests, report the discrepancy, and propose a documented decision; do not quietly assume either is current. Keep roadmap/checklists honest and update documentation with implementation changes.
