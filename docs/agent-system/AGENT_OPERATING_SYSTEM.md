# Universal Task AI — Agent Operating System

This is the canonical index and policy overview for all coding, research, design, integration, QA, and release agents. The detailed policy is split into chapters to make focused reading and prompt attachment easier.

## Mandatory startup for every agent

1. Read the repository root [AGENTS.md](../../AGENTS.md).
2. Read this index and the chapter(s) relevant to your assignment.
3. Read the [Product & Engineering Blueprint](PRODUCT_BLUEPRINT.md), [Design Reference Matrix](DESIGN_REFERENCE_MATRIX.md), and approved page-specific board where your task is visual.
4. Inspect current branch, target commit, current PRs, source files, callers, tests, and CI. These documents describe intent and process; they do not prove present implementation state.
5. Return a bounded implementation proposal before editing: ticket, role/JTBD, scope in/out, owner, dependencies, file allowlist, contract, permissions, failure cases, tests, and expected evidence.

## Core policy

- One product, one design system, one shared set of domain/status/API contracts.
- Research before design; visual reference board before UI implementation; owner approval before production-facing visual build.
- Any design-critical page must have 3–5 relevant visual references, at least two distinct source domains, direct source links, screenshot/image evidence, adopt/reject notes, accessibility/responsive evaluation, and one coherent recommendation. Dribbble/Pinterest/Behance are visual inspiration, not proof of interaction behavior.
- Never copy branded artwork/assets without rights, and never mix unrelated page-specific styles into the product.
- No fake live metrics, fake integrations, fake executions, inert controls, or unsupported success status. Test/demo fixtures must be clearly labeled.
- Preserve the existing codebase and security boundaries. No sweeping rewrites or new framework/dependency without documented reasoning and A0 approval.
- Enforce server-side identity, role permissions, tenant isolation, secret handling, event dedupe/idempotency, bounded execution, audit, and human approval for sensitive side effects.
- Campus integration must use an authorized provider/API and consent. Attendance functionality may remind/open official sources; it must not spoof or silently fabricate official attendance.
- Work on scoped feature/fix/docs branches. Do not work directly on main as normal delivery. Do not merge/deploy/mutate production without required approvals.
- A ticket is complete only with verifiable evidence: acceptance criteria, actual test commands/results, reviewer findings, desktop/mobile screenshots for UI work, limitations, and updated docs. Unrun tests must say NOT RUN.

## Chain of command

**Owner → A0 Architect/Orchestrator → domain specialist → independent A12 review → A0 integration decision → owner approval for high-risk changes.**

A0 alone maintains canonical roadmap, backlog dependencies, ADRs, data/API contracts, visual approval register, file ownership and release recommendations. Specialists must not invent shared schema, state vocabulary, styles or authorization. A12 should review independently from the implementation author; A13 controls release evidence.

## Detailed chapters

- [Chapter 01 — Product Decisions and Agent Ownership](chapters/01-decisions-and-agent-roles.md)
- [Chapter 02 — Quality Gates, Design SOP and Screen Catalog](chapters/02-quality-gates-design-and-screen-catalog.md)
- [Chapter 03 — Shared Flows, API/Security Contracts and Engineering Standards](chapters/03-flows-contracts-and-engineering-standards.md)
- [Chapter 04 — Master System Prompt and Specialist Agent Prompts A0–A13](chapters/04-agent-prompt-library.md)
- [Chapter 05 — Sprint Roadmap, Acceptance Scenarios and Quality Scorecard](chapters/05-roadmap-acceptance-and-scorecard.md)

## Quality gates (G0–G6)

- **G0 Problem/scope:** persona, job-to-be-done, edge cases, scope, risk and acceptance criteria.
- **G1 Visual approval:** page-specific screenshot board, coherent direction, token/component mapping, owner decision. Required before production UI implementation.
- **G2 Contract:** API/schema, tenant scope, permissions, data ownership, state machine, retries and compatibility.
- **G3 Implementation:** assigned branch/path, small vertical slice, tests and docs.
- **G4 Independent review:** security, correctness, UX, accessibility, data integrity, dependencies and license.
- **G5 Evidence:** tests and browser results on the actual implementation, not just mockups. Not-run checks remain NOT RUN.
- **G6 Merge/release:** CI on latest PR head, no unresolved blockers, review, migration/rollback and owner approval for high-risk actions.

## Current starting point

The initial audit (16 October 2026) found the existing FastAPI AI/runtime/security foundations and a draft PR #173 that introduces a Next.js dashboard prototype. The draft's own description says live task submission, workflow persistence and real execution remain unintegrated. It also identified single-global-API-key auth, DEFAULT_USER/in-memory settings, and a not-yet-completed WhatsApp inbound payload mapping in the main branch. Verify these facts against the latest source each sprint; do not treat this snapshot as a permanent truth.

## First milestone

Start at **Sprint 0**: re-audit the current main branch, open PRs and CI; validate PR #173 including CSS build, lockfile/reproducibility and browser screenshots; freeze role/API/data contracts and the cross-page visual system; build a prioritized ticket backlog; do not begin a broad feature rollout until visual and architecture decisions are recorded.
