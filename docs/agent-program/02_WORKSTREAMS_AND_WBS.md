# 02 — Workstreams & Work Breakdown Structure

## Workstream rules

Each epic has one owner, one outcome, a contract, a dependency list and a measurable exit gate. Split implementation into vertical slices that a user can actually exercise. Avoid one epic per technology layer that leaves the whole product disconnected.

| Workstream | Owner | Scope | Deliverables | Key dependencies |
|---|---|---|---|---|
| WS0 Program & Architecture | A0 | product decisions, ADR, contracts, backlog, risk | canonical issue plan and decisions | always |
| WS1 Research & Design System | A1 + A2 | user journeys, source-backed screenshots, tokens, shell, page/role variants | approved reference board + design system | Sprint 0 before production UI |
| WS2 Identity & Data Platform | A3 | auth/session, workspace/member/RBAC, migrations, tenant-scoped repositories | verified isolation and durable data | WS0 |
| WS3 Frontend Workspace | A2 | real app shell, routes, typed API client, state and accessibility | dashboard connected to actual backend | WS1 + WS2 contracts |
| WS4 Tasks & AI | A4 | tasks/projects/backlog, conversations, runs, approvals, artifacts | task-to-artifact journey | WS2 + WS3/API contract |
| WS5 Integrations | A5 | WhatsApp gateway, notifications, one campus connector | event-to-task-to-notification journey | WS2 + WS4 contract |
| WS6 Automation & Developer Studio | A6 | versioned workflow, graph validation, GitHub, diagrams | safe workflow and first useful diagrams | WS2 + WS4; WS5 where triggers used |
| WS7 Quality & Release | A7 | QA, security, integration tests, accessibility, operations readiness | repeatable evidence and readiness gate | every workstream |

## Epic decomposition

### EPIC 0 — Program baseline
- EPIC-0.1 current source/PR/CI audit
- EPIC-0.2 requirements and role/JTBD map
- EPIC-0.3 API/data/state contracts and ADRs
- EPIC-0.4 initial backlog and risk register
- EPIC-0.5 design reference board approval

### EPIC 1 — Identity and persistent workspace
- EPIC-1.1 account/session strategy compatible with local developer mode
- EPIC-1.2 workspaces, membership, roles and permissions
- EPIC-1.3 tenant-scoped settings, runs, approvals and artifact access
- EPIC-1.4 migration strategy, indexes, backup and audit
- EPIC-1.5 cross-tenant negative tests

### EPIC 2 — Real dashboard shell
- EPIC-2.1 inspect and review PR #173
- EPIC-2.2 fix reproducible build/style/lockfile issues
- EPIC-2.3 auth-aware app shell and typed API client
- EPIC-2.4 real health/readiness, run history and truthful UI states
- EPIC-2.5 responsive and keyboard browser tests

### EPIC 3 — Student tasks
- EPIC-3.1 task schema and CRUD
- EPIC-3.2 project and membership
- EPIC-3.3 task detail/checklist/subtasks/labels/dependencies
- EPIC-3.4 list/kanban/calendar views over the same records
- EPIC-3.5 backlog/sprint/milestones after base task flow passes

### EPIC 4 — AI workspace and artifact lifecycle
- EPIC-4.1 conversation and message persistence
- EPIC-4.2 durable async runs/status lifecycle
- EPIC-4.3 approval UI and resume/failure flow
- EPIC-4.4 artifact storage/version/download/access
- EPIC-4.5 usage telemetry, timeout and retry correctness

### EPIC 5 — Integrations
- EPIC-5.1 provider/consent/scope selection
- EPIC-5.2 WhatsApp inbound payload normalization and sender linking
- EPIC-5.3 command routing, idempotency, queue and outbound result
- EPIC-5.4 one authorized campus pilot, sync checkpoints and assignment mapping
- EPIC-5.5 reminder/timezone/preferences/revoke

### EPIC 6 — Automation
- EPIC-6.1 workflow schema/version contract
- EPIC-6.2 graph validation and node I/O contracts
- EPIC-6.3 builder save/load/version
- EPIC-6.4 worker execution with per-step state/retry/timeout/approval
- EPIC-6.5 run inspector, audit and user notification

### EPIC 7 — Developer Studio
- EPIC-7.1 GitHub authorization and repository selection
- EPIC-7.2 repo/issue/PR read context
- EPIC-7.3 ERD source/render/version/export
- EPIC-7.4 flowchart support
- EPIC-7.5 DFD/sequence/UML individually, only after separate validators/renderers/tests

### EPIC 8 — Premium and release
- EPIC-8.1 usage ledger and quotas
- EPIC-8.2 plan entitlement and plan screen
- EPIC-8.3 payment provider and verified webhooks after provider/legal decision
- EPIC-8.4 security/abuse/load/recovery review
- EPIC-8.5 deployment rehearsals, rollback and real production readiness

## Scope control

An epic is not one ticket. Each implementation ticket should typically target one coherent, reviewable slice. If scope expands, A0 updates acceptance criteria and dependencies before work continues. Features blocked by missing provider access, credentials or owner choice remain BLOCKED, not implemented using a fake integration.
