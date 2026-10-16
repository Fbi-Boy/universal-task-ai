# 01 — Team Topology: How Many AI Agents?

## Recommendation

The repository already defines canonical agent IDs A0–A13 in docs/agent-system/chapters/01-decisions-and-agent-roles.md. This program reuses those exact IDs. Do not renumber them or create a second incompatible A0–A7 system.

Do **not** run 14 independent agents simultaneously. Use **4 active agent sessions for Sprint 0**, then normally **6 active sessions during implementation**, with **7 as the practical maximum** until coordination is proven. All specialist roles remain available in the catalog, but they are activated only when their dependency is ready.

## Canonical roles (reuse the existing IDs)

| ID | Role | Primary output | Not allowed |
|---|---|---|---|
| A0 | Chief Architect / Program Orchestrator | backlog, dependencies, ADRs, contracts, file ownership, integration decision | waive owner approval, claim evidence without checking, review own work as independent QA |
| A1 | Product & Student Workflow Researcher | product requirements, user journey, personas/roles, acceptance criteria | implement production UI from unapproved assumptions |
| A2 | Design Research & Visual Reference Curator | screenshot research, source-backed visual board, adopt/reject rationale | treat visual inspiration as proof of product behavior or license to copy artwork |
| A3 | Design System Steward / Design QA | shared tokens/components, visual consistency, accessibility and screenshot review | add unrelated per-page design language |
| A4 | Frontend Platform & App Shell Engineer | Next.js shell/routes, typed API client, truthful states, browser integration | invent API contracts or fake live data/status |
| A5 | Identity, Workspace & Data Platform Engineer | auth/session, workspace/RBAC, migrations, tenant-safe data access | trust user/workspace IDs supplied by an untrusted request |
| A6 | Student Tasks, Projects & Backlog Engineer | durable tasks, projects, views, dependencies, sprint/backlog | create separate inconsistent stores for different views |
| A7 | AI Workspace, Runs & Artifact Engineer | conversations, AI run lifecycle, approvals, artifact versions/provenance | bypass permission boundary or claim unsupported work completed |
| A8 | WhatsApp, Notification & Campus Connector Engineer | verified inbound/outbound messages, authorized campus sync, notification delivery | unauthorized scraping, hidden official actions or credential exposure |
| A9 | Workflow Automation Engineer | versioned workflow schema, safe execution, run/step logs, retry/approval | let canvas or model grant itself runtime permission |
| A10 | Developer Studio Engineer | GitHub scopes/repository access, diagrams, versioning and export | claim formats work without parser/render/export tests |
| A11 | Subscription, Usage & Plans Engineer | usage ledger, quotas, entitlements, payment provider flows | invent pricing/usage/payment state or handle raw card data |
| A12 | Independent QA, Security & Reliability Reviewer | reproducible findings, automated tests, threat/accessibility review | accept implementer self-report as proof or waive product-owner release approval |
| A13 | DevOps / Release Steward | reproducible builds, migrations, monitoring, backups and rollback evidence | deploy or mutate production without explicit approval |

These are role profiles, not a requirement to maintain 14 separate always-on AI sessions.

## Active capacity by phase

### Sprint 0 — 4 active sessions maximum
Use A0 (coordination), A1 (requirements), A4 (audit PR #173/current frontend and run build checks), and A12 (independent security/test review). A2 can take the next sequential ticket after A1 provides the page brief; do not add a fifth concurrent session simply to overlap research.

### Normal implementation — 6 active sessions
A0 always coordinates and A12 provides independent review. Select up to four domain agents from A2–A11 whose dependencies are satisfied. The exact group depends on the sprint. Examples:
- Auth/data vertical slice: A0 + A5 + A4 + A6 + A12 + one integration tester/domain specialist.
- WhatsApp-to-artifact slice: A0 + A5 + A7 + A8 + A12 + A4.
- Workflow slice: A0 + A7 + A9 + A4 + A12 + one relevant data/domain specialist.

### Practical maximum — 7 active sessions
A seventh session is permitted only if contracts and file ownership are stable, an independent reviewer is available, and each agent's changes can be integrated without overlapping shared files. If agents are waiting on each other or creating conflicting API/schema/style decisions, reduce parallelism.

### A11 and A13 are phase-activated
Billing/payment integration (A11) and production release work (A13) are not needed in every sprint. Activate them only after usage/payment contracts or release prerequisites exist. A13 must not deploy without owner approval.

## Reporting and shared-file ownership

Product Owner → A0 → domain owner → A12 independent review → A0 integration recommendation → product owner approval for high-risk choices.

A0 must name one primary owner for any shared path in a work window. Examples: OpenAPI schemas, migrations, global design tokens, shared app shell, root AGENTS.md, workflow status schema, and program-state records. No two agents may write the same shared file in parallel without an explicit coordinated change.

## Rules for creating subagents

Create a temporary subagent only when the task is sizeable and independent, has a separate acceptance/test plan, has a clear owner/path scope, and saves more time than its coordination cost. Tiny subtasks remain under the parent ticket. Never spawn several agents to “review everything” without assigning distinct review checklists.
