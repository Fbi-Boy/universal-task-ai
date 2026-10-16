# 07 — Shared Contract Register

This is a register, not a substitute for API schemas. Each contract has one owner and versioned source. Before a dependent ticket starts, its relevant contract must be status FROZEN or the ticket must explicitly be contract discovery.

## Contract lifecycle

DRAFT → REVIEW → FROZEN → IMPLEMENTED → VERIFIED.

- **DRAFT:** proposal; dependent implementation should not assume stability.
- **REVIEW:** domain owners, A0 and QA review semantics, permissions, failure cases and compatibility.
- **FROZEN:** consumers can build in parallel against the exact contract revision.
- **IMPLEMENTED:** owning service/UI exists.
- **VERIFIED:** tests and integrated acceptance scenario prove behavior.
- If a frozen contract needs change, create an ADR/change note, list impacted tickets, coordinate rollout/migration, and notify every consumer before code changes.

## Current vs target API surface

The following existed in the main branch at initial audit; verify exact request/response schemas from the current source before use:
- POST task analysis and POST task run under /v1/tasks
- tool catalog under /v1/tools
- run list/detail and run events under /v1/runs
- approval router and settings routes
- health and readiness endpoints

Do not infer endpoint support just from this list. Read API code/OpenAPI, auth dependencies, response models, tenant scoping, event persistence and tests.

The following are **target API groups, not claims of current implementation**:
- Auth/workspaces/members and invitations
- Projects/tasks/backlog
- AI conversations and durable job submission/status/cancellation
- Artifacts/versions/downloads
- Campus connectors/assignments/sync status
- WhatsApp webhook/account-linking/notification preferences
- Workflow definitions/versions/runs/step history
- GitHub connections/repository selection/issues/PR context
- Diagram documents/source/validation/render/export
- Usage/plan/entitlements/payment webhooks
- Audit/security administration

## Shared domain contracts

| Contract ID | Definition | Owner | Consumers | Initial status |
|---|---|---|---|---|
| C-001 | Authenticated actor/session/workspace context | A5 | all APIs, workers, integrations | NEEDS DESIGN |
| C-002 | Role + resource/action permission policy | A5 | all domain APIs and background jobs | NEEDS DESIGN |
| C-003 | Error envelope, request ID, validation errors | A0 + A5 | frontend and all APIs | NEEDS DESIGN |
| C-004 | Common task/project identifiers and tenant ownership | A5 + A6 | Tasks, Campus, AI, Developer Studio | NEEDS DESIGN |
| C-005 | Task status and transition rules | A6 + A0 | frontend, campus and automation | NEEDS DESIGN |
| C-006 | Run/job state machine and async response | A7 | UI, workers, notifications, workflows | NEEDS DESIGN |
| C-007 | Artifact ownership/version/download contract | A7 + A5 | AI, tasks, notifications, developer tools | NEEDS DESIGN |
| C-008 | Integration connection/credential/revoke schema | A5 + A8 | campus, WhatsApp, GitHub, model providers | NEEDS DESIGN |
| C-009 | Inbound/outbound notification event and delivery state | A8 | campus, WhatsApp, task/run | NEEDS DESIGN |
| C-010 | Campus event normalize/dedupe/checkpoint schema | A8 + A6 | campus connector, task service | NEEDS DESIGN |
| C-011 | Workflow node/edge/input/output schema | A9 + A0 | canvas, validator, executor | NEEDS DESIGN |
| C-012 | Workflow run/step status/retry/approval | A9 + A7 | builder, workers, notification | NEEDS DESIGN |
| C-013 | Diagram source/version/format/export contract | A10 + A0 | diagram editors, artifact storage | NEEDS DESIGN |
| C-014 | GitHub connection scopes and repository ownership | A10 + A5 | Developer Studio | NEEDS DESIGN |
| C-015 | Usage event/quota/entitlement semantics | A0 + A7 + A5 | worker, billing, UI | NEEDS DESIGN |
| C-016 | Owner-approved design tokens/components | A2 + A3 | all UI pages and roles | NEEDS APPROVAL |
| C-017 | Webhook signature/idempotency/replay protection | A8 + A5 | WhatsApp and provider callbacks | NEEDS DESIGN |
| C-018 | Audit event and redaction schema | A5 + A12 | security-sensitive domain operations | NEEDS REVIEW |

## Contract record template

For each contract, document:
- Contract ID, version, status, owner and date.
- Request/response/entity schemas and validation bounds.
- Authenticated actor/workspace and permissions.
- Success, partial, validation, retry, timeout and failure semantics.
- Idempotency/ordering/cancellation behavior.
- Data retention, secrets/redaction and audit requirements.
- Consumers, migration/compatibility notes and fixtures.
- Test files and verified acceptance scenario.

No frontend mock or generated SDK becomes authoritative until it matches the approved schema.
