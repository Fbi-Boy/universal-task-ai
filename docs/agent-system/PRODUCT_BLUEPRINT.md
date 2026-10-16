# Universal Task AI — Product & Engineering Blueprint

This blueprint translates the product vision into a modular delivery plan. It is a target design, not a claim that all listed modules already exist. Verify the live repo and PRs before each sprint.

## Product goal

Build a student productivity and IT developer workspace that unifies:

- AI workspace with conversations, task planning, secure runs, approvals and saved artifacts.
- Tasks, projects, backlog, kanban/list/calendar, deadlines and collaboration.
- Authorized campus assignment/event detection, notifications and WhatsApp commands.
- Visual automation workflows inspired by node-based automation tools, with real persistence and safe background execution.
- Developer Studio for GitHub context and versioned ERD/DFD/flowchart/sequence/UML diagrams, implemented incrementally.
- Integrations, settings, usage metering, plan entitlements and later billing.

## Current-repo observations to reverify

The audit of 16 October 2026 found a useful FastAPI/Python task and AI runtime, model gateway patterns, tool boundaries, approvals, audit/run state, scheduler primitives, diagram validators, WhatsApp adapter primitives and CI/deployment workflows. The previous web UI under backend/web is a basic single-page workspace. PR #173 is a draft Next.js dashboard/visual workflow prototype; its description states metrics/activity are illustrative and live task submission, workflow persistence, drag/drop and execution are not connected. Current auth uses a configured global API key; settings are tied to DEFAULT_USER and in-memory storage; WhatsApp inbound payload mapping contains NotImplementedError. Recheck these against the latest branch, PR and test run before relying on this snapshot.

## Recommended architecture

Use a **modular monolith first**: Next.js + TypeScript for the hosted dashboard after review, FastAPI for authenticated domain APIs and the existing secure task runtime, PostgreSQL for multi-user product data, Redis/worker for long-running jobs, object storage for artifacts, and adapters for each external provider. Existing SQLite may remain for local development/testing while migrations are staged. Do not create a second backend or split into microservices without measured need.

All entry points converge on one trusted task pipeline:

```text
Dashboard / verified WhatsApp / authorized campus event / schedule / authorized GitHub event
  -> normalize + deduplicate
  -> resolve identity + workspace + consent + permissions
  -> create durable task/run + idempotency key
  -> queue + worker
  -> analyze + plan
  -> approval if sensitive
  -> execute through existing permissioned tool/runtime boundary
  -> validate/review output
  -> persist versioned artifact + provenance
  -> notify and expose truthful run state
```

Common statuses: queued, running, needs_input, waiting_approval, ready_for_review, completed, failed, cancelled, retrying. Never mark unsupported or failed work as successful.

## Domain data and API concepts

Core entities include users/auth identities/sessions/workspaces/members; projects/tasks/comments/checklists/dependencies; conversations/messages/runs/steps/events/approvals; artifacts/versions/sources; integration connections/credential references/webhook events; campus connections/courses/assignments/schedules/checkpoints; workflows/versions/nodes/edges/runs/step-runs; GitHub connections/repositories/diagram documents/versions; plans/subscriptions/usage events/audit logs.

Use server-derived identity and workspace scope; enforce RBAC/tenant boundaries on API, database queries, background jobs, artifact access, events and connectors. Standardize versioned API schemas, typed client, pagination, stable safe error shape, request IDs, idempotency, bounded request sizes, provider timeouts and webhook replay protection. Store credentials encrypted and never expose or log secrets.

## Delivery chapters

- [Product, workflows, architecture and data model](chapters/blueprint-01-product-and-architecture.md)
- [API groupings, sprint roadmap and agent dependencies](chapters/blueprint-02-api-and-sprint-roadmap.md)
- [Specialist prompts and coordination templates](chapters/blueprint-03-specialist-prompts-and-coordination.md)
- [Agent operating rules](AGENT_OPERATING_SYSTEM.md)
- [Design reference board](DESIGN_REFERENCE_BOARD.html)
- [Design reference matrix](DESIGN_REFERENCE_MATRIX.md)

## Product integrity and rollout rules

- Campus connector support must name the actual provider and authorized API/consent; do not assume a generic LMS or silently scrape credentials.
- Attendance features may notify, schedule reminders and open official links. Do not spoof attendance, identity, location or official verification. Treat assignment outputs as drafts for user review; an official submission requires supported platform rules and explicit confirmation.
- Prefer implementing a narrow, usable vertical slice over many disconnected screens. No fake metrics, no mock integration labeled connected, no inert controls, no workflow node with self-granted authority.
- Evaluate current licensing terms before embedding or offering user-editable n8n workflows as part of a commercial service.
- A local smoke test or production rehearsal is not a successful real production rollout. Release requires immutable build, current CI, migration/backup/rollback plan, monitoring/health checks, verified end-to-end flow and owner approval.
