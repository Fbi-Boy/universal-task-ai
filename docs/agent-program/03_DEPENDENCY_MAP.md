# 03 — Dependency Map & Parallelization

## Dependency chain

Program dependencies should be resolved in this order:

1. Current repo/PR/CI audit and product decisions.
2. Requirements, role matrix, data/API/state contracts, threat boundaries.
3. Design reference boards and owner approval for first representative screens.
4. Identity/session/workspace and tenant-safe data foundation.
5. Real frontend shell/API client and one usable task flow.
6. AI run + artifact end-to-end.
7. WhatsApp gateway, then one campus connector.
8. Versioned workflow runtime/builder.
9. GitHub/diagram Developer Studio.
10. usage/plan/billing.
11. system hardening, production rehearsal and owner go-live decision.

## Safe parallelism matrix

| Work pair | Parallel? | Condition |
|---|---|---|
| Product research + visual research | Yes | Shared page/role requirements documented |
| UI implementation + backend API | Yes, after G2 | Frozen OpenAPI/schema and named file owners |
| Auth/data migration + task CRUD | Limited | Migration owner A3 only; task engineer uses approved schema |
| AI runtime + frontend AI screen | Yes, after contract | Same run-state/status/API contract |
| WhatsApp adapter + task service | Yes, after contract | Normalized command/event schema and stable task/run API |
| Campus provider research + app shell | Yes | Research does not edit frontend/backend shared files |
| Workflow canvas UI + workflow API | Yes, after schema | Node/edge schema, validation and state lifecycle approved |
| Different diagram types | Limited | Each has own source grammar and validator; shared canvas API frozen |
| Shared auth/permissions/token CSS/migrations | No by default | Single owner/change window or explicit design/code review |
| Billing screen + billing state machine | Yes, after contract | Provider webhook, quota semantics and entitlement contract frozen |
| Implementation agent + independent QA | Sequential for final gate | QA must inspect actual diff and evidence, not just design plan |

## Mermaid dependency map

A0 initializes the program and confirms requirements. Product/design research can proceed alongside source audit. API/data contracts gate frontend/backend parallel work. Integration and automation depend on durable identity, tasks/runs and event contracts. Independent QA reviews every slice and blocks incomplete work.

flowchart TD:
- A0[Program audit and decisions] --> SPEC[Requirements, data/API contracts]
- A1[Product/design research] --> VIS[Approved visual references and design system]
- SPEC --> ID[Identity, workspace and persistence]
- VIS --> FE[Frontend shell and page components]
- ID --> API[Real tenant-scoped APIs]
- API --> TASK[Tasks/projects/backlog]
- API --> AI[AI runs and artifacts]
- TASK --> CAMPUS[Campus + WhatsApp integration]
- AI --> CAMPUS
- AI --> AUTO[Workflow runtime and builder]
- ID --> DEV[GitHub and Developer Studio]
- AUTO --> QA[Independent quality/security gate]
- CAMPUS --> QA
- DEV --> QA
- FE --> QA
- QA --> REL[Release readiness]
- REL --> OWNER[Owner go-live approval]

## Merge integration rules

- Every agent branches from the agreed latest base and opens a PR.
- No parallel edit to the same migration, OpenAPI schema, shared types, shared tokens, app shell navigation or root instructions without A0 assigning one owner.
- Contract changes are announced before dependent branches implement against them.
- A0 merges the integration plan only after reviewing dependency completion, conflicts, CI and A7 report.
- If a contract must change, stop dependent work, propose migration/backward-compatibility changes, then notify all affected agents.
