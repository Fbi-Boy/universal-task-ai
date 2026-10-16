## 10. Sprint roadmap with dependencies

### Sprint 0 — Re-audit and freeze decisions

- Refresh `main`, open PRs, CI, diffs, branch protection, latest tests and current local/hosted run strategy.
- Review PR #173, repair CSS/lockfile/CI/browser smoke blockers; check visual screenshot with owner.
- Set up canonical docs: PRD, roles/permissions, system context diagram, ADR log, reference board index, API contracts, threat model, sprint backlog.
- Output: baseline audit, prioritized backlog, architecture decisions and no-merge list.

### Sprint 1 — Research and design system approval

- Create cross-page reference board, choose global visual direction, typography, color tokens, spacing, shell, states and reusable component inventory.
- Owner approves main shell and 2 representative pages before broad implementation.
- Output: design tokens, page templates, design reference matrix and screenshot acceptance rubric.

### Sprint 2 — Multi-user identity and tenant data

- Users/auth/session/workspaces/members/RBAC/migrations; move API key global flow to a compatible supported auth architecture.
- Scope all settings, runs, approvals, artifact access and job context; add cross-tenant tests.
- Output: secure workspace skeleton; existing local mode still testable.

### Sprint 3 — Real frontend/API foundation

- Connect Next.js app shell to real health/auth/workspace endpoints, route protection, typed client, error handling and responsive layout.
- Replace fake profile/workspace/health/metrics. Implement loading/empty/error states.
- Output: navigable real shell, no false data.

### Sprint 4 — Tasks, Projects and Backlog vertical slice

- Task list/detail, priority, deadlines, checklist, labels, list/kanban, project/backlog/milestone basics, search/filter/pagination.
- Output: create/update/reassign and verify persisted tasks under workspace policy.

### Sprint 5 — AI Workspace + Run + Artifact end-to-end

- Chat/conversation, task run, plan/activity/status timeline, approval states, file artifact/version, retry/error. Use current model gateway/runtime.
- Output: one completed user-to-run-to-artifact journey with provenance and truthful statuses.

### Sprint 6 — WhatsApp account linking and command pipeline

- Provider/webhook verification, inbound schema map, user link, command parser, dedupe, async queue, outbound updates, opt-in/revoke.
- Output: test provider or sandbox demonstrates new-task notification → command → job → saved artifact → WhatsApp result.

### Sprint 7 — Campus Hub pilot

- Choose one supported and authorized LMS/notification source; establish OAuth/token or permitted integration flow; assignment sync/checkpoint/dedupe; reminder settings/timezone.
- Output: one connector proven in sandbox/test account. Presensi is reminder/open official link, not spoofed action.

### Sprint 8 — Workflow builder and execution monitor

- Versioned workflow schema, graph validation, trigger/action/condition registry, run/step states, retries/approval and execution inspector. UI based on approved board and selected node canvas library.
- Output: schedule/manual/webhook trigger through a real safe flow with run history.

### Sprint 9 — Developer Studio

- GitHub connection/scopes, selected repositories, repository/issue/PR context, ERD and flowchart editor/export. Add DFD/sequence/UML incrementally with independent acceptance.
- Output: at least one valid diagram workflow saved as versioned artifact and repository context secured.

### Sprint 10 — Usage, plan and internal operations

- Meter model/action executions, limits, plan entitlement, payment gateway integration, customer plan screen, platform admin operations with separated privileges.
- Output: quotas enforced server-side, verified payment/webhook tests, audit records.

### Sprint 11 — Production hardening

- Load/concurrency, worker recovery, backups/restore, queue retry/dead letter, tenant isolation, rate limiting, monitoring/alerts, browser E2E, accessibility and full threat review.
- Output: documented production readiness review, deploy/rollback proof and owner go-live approval.

Each sprint is a set of small PRs; do not make one mega PR per sprint. The milestone passes only when its defined vertical slice is integrated and verified.

---

## 11. End-to-end acceptance scenarios (must stay green)

1. **New user:** signs in, creates workspace, sees empty states (no fabricated metrics), configures timezone, can revoke own session.
2. **Tenant isolation:** user A cannot retrieve user B task, run, artifact, workflow, file, integration, audit row or live event by guessing ID.
3. **Task flow:** user creates task with due date, opens detail, changes status, refreshes, and sees persisted state.
4. **AI run:** task accepted → queued → running → actual result/needs_input/failed → run history updates without fake success.
5. **Artifact flow:** generated draft is associated with right task/workspace, versioned, downloadable only by authorized users, and contains metadata/provenance.
6. **WhatsApp flow:** unknown sender rejected/linked correctly; invalid signature rejected; valid message acknowledged; duplicate provider event does not create duplicate run; outbound error retries safely.
7. **Campus sync:** connector can revoke, detects duplicates, respects checkpoints, handles deleted/changed assignments and timezone/deadline display.
8. **Attendance reminder:** sends scheduled reminder and opens official link; product does not claim to have performed attendance.
9. **Automation flow:** draft → validation → save version → run → per-step timeline → approval pause/resume or truthful failure → retry without duplicate side effects.
10. **GitHub:** least-privilege connection, explicit repository selection, permission error on unlinked repo, revoke stops further access.
11. **ERD/flowchart:** create/update, validate good/bad input, persist version, re-open, export and compare output.
12. **Usage limit:** nearing/exceeding quota is clear; backend blocks or requests plan change; failed jobs are metered according to documented rule.
13. **Mobile:** app navigation, forms, board actions, chat composer and diagram fallback remain usable at narrow viewport.
14. **Production readiness:** tests run at exact release commit; health/readiness, worker, database, queue, storage, notification, backup and rollback all verified.

---

## 12. Sprint and agent coordination template

Copy this template when assigning work:

```text
UTA TICKET: UTA-XXX — <title>
SPRINT: <n>
PRIMARY AGENT: A<n>
REVIEWERS: A0, A12, and domain-specific reviewer
BRANCH: feat/UTA-XXX-<slug>
DEPENDENCIES: <ticket/contract/ADR IDs>

PROBLEM / USER ROLE:
<job-to-be-done, current pain>

SCOPE IN:
- ...
SCOPE OUT:
- ...

FILES / OWNERSHIP:
Allowed paths: ...
Do not modify: ...
Shared APIs/tokens touched: ...

APPROVED DESIGN REFERENCE:
<board path and approval record; N/A only for nonvisual backend work>
API / DATA CONTRACT:
<OpenAPI/schema/ADR path>

ACCEPTANCE CRITERIA:
1. Given ... when ... then ...
2. ...

SECURITY / FAILURE CASES:
- cross-tenant access
- missing/expired permission/credential
- duplicate event/retry
- timeout/partial failure
- untrusted payload / malformed output

TEST PLAN:
- <exact command>
- <integration/E2E/manual check>

DELIVERABLES:
- Code + tests + docs + migration as applicable
- PR + screenshot + test evidence
- Known limitations/follow-up ticket

EXIT GATE:
No merge until A12 has reviewed, required CI passes on final PR HEAD, and A0 approves integration.
```

### Daily/iteration coordination message

```text
A0 coordination report — <date/commit>
- Current milestone and objective:
- Agent state: READY / ACTIVE / BLOCKED / REVIEW / DONE (evidence required for DONE)
- Branch/PR and changed paths:
- Contract shared or changed:
- Conflicts/dependencies:
- Tests/review evidence:
- Risks/blockers and decision needed from owner:
- Next assigned ticket:
```

---

## 13. Quality scorecard — no completion percentages without evidence

Score 0/1/2 for every category: 0 = absent/failing, 1 = partial/unverified, 2 = verified with evidence. Any critical security category at 0 blocks acceptance.

| Category | Evidence for score 2 |
|---|---|
| Product fit | Acceptance criteria map to real task and role; owner approves scope |
| Visual coherence | Approved reference board + screenshot comparison + shared tokens/components |
| Functionality | Actions connect to real API and persisted state; no fake success |
| Authorization | Server-side RBAC plus cross-tenant regression tests |
| Reliability | Timeouts/retries/idempotency/interruption covered for async flows |
| Data integrity | Constraints/migrations/ownership and backup/recovery considered |
| Accessibility | Keyboard/focus/labels/contrast/responsive checks documented |
| Tests | Relevant automated checks actually ran on latest revision |
| Documentation | API/ADR/runbook/limitations current |
| Operations | Logs/metrics/readiness/release/rollback evidence appropriate to stage |

Acceptance suggestion: at least 18/20 and no 0 in Authorization, Data Integrity, Tests, or Security. This is a project gate, not a claim of formal certification.

## 14. Official and visual reference starting library

Use the companion visual board to inspect screenshots. Reference links for verified implementation/pattern research:

- [shadcn/ui official source](https://github.com/shadcn-ui/ui) — composable UI elements, source available for customization; check exact package/license and version.
- [shadcn/ui component documentation](https://ui.shadcn.com/docs/components) — accessible interaction patterns and reusable primitives.
- [React Flow / xyflow](https://github.com/xyflow/xyflow) — node-based editor/canvas option for workflow and diagram builders; evaluate current version and license before adoption.
- [Eraser Diagrams](https://github.com/eraserlabs/eraser-diagrams) — diagrams-as-code and consistent diagram conventions to evaluate for generated technical artifacts.
- [ClickUp task views](https://help.clickup.com/hc/en-us/articles/6310383076503-Task-views) — source for task list/board/calendar/timeline behavior, not a design to copy.
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) — issue/project relationships and flexible planning workflow.
- [n8n documentation](https://docs.n8n.io/) — workflow behavior and operations; evaluate n8n licensing/terms before offering embedded/customer-configurable n8n.
- [Next.js docs](https://nextjs.org/docs) — framework routing, rendering and deployment behavior.
- [FastAPI docs](https://fastapi.tiangolo.com/) — backend API patterns.

The reference board includes visual inspiration links for dashboard overview, AI chat, task/kanban, workflow canvas, ERD, and GitHub project views. Always check original pages, update the gallery before a new page sprint, and do not use inspiration images as product assets without rights.

## 15. Go/no-go right now

**GO:** Sprint 0 repository/PR audit; source-backed design research; design system proposal; architecture/contracts; test gaps inventory.

**NO-GO for broad build-out until cleared:** merging PR #173 unreviewed; marking draft metrics as real; announcing WhatsApp/Canvas/LMS/GitHub/billing as production-ready; allowing multiuser access through one global API key; enabling a workflow node to bypass the existing tool security boundary; automating attendance/submission without policy and explicit approval.

**Immediate next action:** assign A0 + A2 + A3 to finish Sprint 0 and the cross-page visual reference board. Owner reviews the gallery and the chosen global direction, then A5 can begin the tenant/auth design while A4 prepares only the approved frontend foundation. A6/A7/A8/A9 can proceed in parallel after contracts and path ownership are recorded.
