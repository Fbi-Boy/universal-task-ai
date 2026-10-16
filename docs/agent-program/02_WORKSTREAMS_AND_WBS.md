# 02 — Workstreams & Work Breakdown Structure

Role IDs in this file follow the canonical A0–A13 catalog in docs/agent-system/chapters/01-decisions-and-agent-roles.md. Do not create a second numbering scheme.

## Workstreams

| Workstream | Owner | Scope | Deliverable | Depends on |
|---|---|---|---|---|
| WS0 Program & Architecture | A0 | requirements, ADRs, contracts, backlog, risk, integration | canonical decisions and issue plan | always |
| WS1 Product & Visual Research | A1 + A2 | personas, flows, screenshot references, role/page matrix | owner-reviewed product/design brief | Sprint 0 |
| WS2 Design System | A3 | tokens, shared components, responsive/accessibility rules | one approved visual system | WS1 |
| WS3 Frontend Workspace | A4 | Next.js app shell/routes, typed API client, real UI states | dashboard connected to actual API | WS2 + frozen contracts |
| WS4 Identity & Data Platform | A5 | auth/session, workspace/RBAC, migrations, tenant-scoped repositories | durable and isolated data | WS0 |
| WS5 Tasks & AI | A6 + A7 | tasks/projects/backlog, conversation, runs, approvals, artifacts | task-to-artifact vertical slice | WS4 + API contracts |
| WS6 Integrations | A8 | WhatsApp, notifications, one authorized campus connector | event-to-task-to-notification path | WS4 + WS5 |
| WS7 Automation & Developer Studio | A9 + A10 | workflow schema/runtime, GitHub, diagrams | safe workflow and first useful diagrams | WS4 + WS5 |
| WS8 Usage & Billing | A11 | usage ledger, quota, plans, provider payment integration | truthful metering/entitlement | usage contract |
| WS9 Quality & Release | A12 + A13 | independent QA/security, accessibility, deployment readiness | evidence-backed release gate | every workstream |

## Epic decomposition

### EPIC 0 — Program baseline
- E0.1 audit main, in-flight PRs, CI, deployments and actual capabilities
- E0.2 requirements, personas, role/permission map and high-risk assumptions
- E0.3 API/data/status/error contracts and architecture decision records
- E0.4 source-backed visual board and design-system direction
- E0.5 prioritized GitHub Issues/Project and risk register

### EPIC 1 — Identity and durable workspace
- E1.1 session/auth strategy that preserves a secure local developer mode
- E1.2 user, workspace, membership, roles and authorization model
- E1.3 tenant-scoped settings, run history, approvals, events and artifacts
- E1.4 migration/index/backup/audit strategy
- E1.5 cross-tenant negative tests and access review

### EPIC 2 — Real dashboard shell
- E2.1 review PR #173 and current frontend source
- E2.2 fix verified CSS/build/lockfile/CI issues in scoped PRs
- E2.3 auth-aware shell and typed API client
- E2.4 real health/readiness, run history and truthful UI states
- E2.5 responsive, keyboard and browser smoke tests

### EPIC 3 — Student tasks and projects
- E3.1 persisted task/project schema and CRUD
- E3.2 task detail, due dates/timezone, priority, labels, checklist, subtasks and dependencies
- E3.3 list/kanban/calendar views over the same task records
- E3.4 project backlog/sprints/milestones once basic task flow passes
- E3.5 search/filter/pagination and workspace authorization

### EPIC 4 — AI workspace and artifacts
- E4.1 persisted conversations/messages with privacy boundary
- E4.2 durable async jobs/run status, retry, timeout, resume/cancel semantics
- E4.3 plan, tool activity, approval, review and failure UI
- E4.4 artifact versions, provenance, access-controlled download and retention
- E4.5 provider errors and real usage events

### EPIC 5 — WhatsApp and campus
- E5.1 provider, scopes, consent and connector lifecycle
- E5.2 verified WhatsApp payload parsing and sender/account linking
- E5.3 command router, idempotency, queued run and outbound status
- E5.4 one authorized campus connector and assignment sync checkpoints
- E5.5 due-date/timezone/reminder preferences and revocation

### EPIC 6 — Workflow automation
- E6.1 typed, versioned workflow schema
- E6.2 graph validation, node input/output and permission policy
- E6.3 builder save/load/version and workflow publishing
- E6.4 worker execution with per-step logs, retry, timeout, approval and cancellation
- E6.5 execution inspector, audit, notification and resume/recovery

### EPIC 7 — Developer Studio
- E7.1 secure GitHub connection and explicit repository selection
- E7.2 repository/issue/PR context with least privilege
- E7.3 ERD source/render/version/export vertical slice
- E7.4 flowchart source/render/version/export
- E7.5 DFD/sequence/UML individually after their parser/render/export acceptance tests

### EPIC 8 — Usage, billing and release
- E8.1 usage ledger, event idempotency and quota contract
- E8.2 server-side entitlements and plan UI
- E8.3 choose payment provider only after product/legal/operational review
- E8.4 verified payment webhooks and reconciliation tests
- E8.5 security/load/recovery, monitoring, backup/restore and rollback rehearsal

## Scope control

An epic is not one ticket. Every delivery ticket targets one coherent slice that is demonstrably usable. A0 updates acceptance/dependencies before expanding scope. Missing provider access, credentials, approval or legal/licensing decision makes the ticket BLOCKED, not an invitation to fake the integration.
