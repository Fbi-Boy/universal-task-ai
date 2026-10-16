# 00 — Program Charter

## Mission

Deliver Universal Task AI as a coherent student productivity and IT developer workspace. It should combine AI chat/task execution, tasks/projects/backlog, authorized campus assignment tracking, WhatsApp notifications/commands, durable artifacts, visual automation, GitHub integration, ERD/DFD/flowchart/UML tooling, settings, and later usage plans.

The aim is not to build several disconnected demos. The aim is one authenticated workspace in which the same user, project, task, execution, artifact, workflow, integration, permission and audit concepts work together.

## Project outcomes

1. Students can track deadlines and tasks in one place.
2. AI can explain, draft, research and complete bounded permitted work, with truthful execution status and saved artifacts.
3. Campus events and WhatsApp commands enter the same authorized task pipeline and are deduplicated.
4. Projects, tasks, conversations, workflow runs and artifacts have durable ownership and tenant boundaries.
5. IT users can work with GitHub context and technical diagrams.
6. Workflows can be designed, versioned, safely executed, inspected and resumed.
7. Premium/usage limits are enforced in backend services, not only hidden in the UI.
8. Each UI route follows one owner-approved, evidence-backed design system.
9. Every release is reviewable, testable, auditable and reversible.

## Scope order

Build the foundations first: existing-repo audit → design system and product contracts → identity/workspace/tenant persistence → real dashboard/API integration → task/project vertical slice → AI run/artifact vertical slice → WhatsApp → one authorized campus pilot → workflow engine → Developer Studio → usage/billing → production hardening.

Scope is intentionally phased. “Future feature” is not permission to create an unconnected screen or fake data. Do not build every feature at once.

## Decision authority

- **Product Owner (human):** final authority for product direction, page design approval, significant scope/budget/privacy tradeoffs, merge policy and production deployment.
- **A0 Program Orchestrator:** responsible for converting owner intent into issues, dependencies, contracts, ADRs, assignments and integration decisions. A0 may reject work that violates shared standards.
- **Workstream Owner:** owns implementation and technical report for a bounded domain.
- **A7 Independent QA/Security:** reviews independently and can block a ticket with reproducible issues; cannot waive owner permission.
- **Other agents:** propose options and implement tickets, but may not rewrite global contracts or silently expand scope.

## Non-negotiable rules

- Keep current working code; inspect the latest source/branch/PR before proposing changes.
- Research before design. A page cannot enter production implementation without a visual reference board and owner approval.
- One shared set of design tokens, component APIs, state vocabulary, auth/tenant policy and API contracts.
- No fake metrics, fake integration status, false completion, or unlabelled prototype.
- No tool permission can be granted by a model response or workflow definition alone.
- Cross-tenant data access is always denied unless the explicit sharing policy authorizes it.
- Campus and messaging integrations require correct consent, provider authorization, secure credentials and deduplication.
- No spoofed attendance, identity deception or silent official academic submission. Treat generated academic work as a draft for review; external submission requires a supported/allowed platform path and explicit confirmation.
- Never commit credentials or real student data to fixtures, source or screenshots.
- Never report a test as passing if it was not actually run.
- No production action or merge of a risky change without required review/approval.

## Source-of-truth hierarchy

1. Current repository source, current CI and current deployed state where verifiable.
2. Approved API/data contracts and ADRs in version control.
3. GitHub Issues/Project for current status, owner, dependencies and acceptance.
4. Approved page-specific design boards and design decision records.
5. These program documents for work methodology.
6. Chat and prior AI responses for context only.

If these conflict, agents stop, report the conflict and ask A0 to update the authoritative record. Do not silently create a second truth.

## Successful program criteria

A feature is accepted when its user-visible outcome works end-to-end, contracts and permissions are enforced server-side, states/errors are truthful, tests and independent review provide evidence, design matches the approved reference, and operational/documentation impact is recorded. Feature count and lines of code are not success measures.
