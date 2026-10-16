# 09 — Sprint 0 Runbook: What Happens First

## Goal

Create a trustworthy baseline, not new features. Sprint 0 must establish what exists, what is prototype-only, which contracts need decisions, which design references are approved, and which tickets can start safely.

## Capacity: maximum four active AI sessions

Use these roles concurrently:
- **A0:** orchestrates audit, decisions, issue plan and program state.
- **A1:** documents user journeys, requirements, personas/roles and provider questions.
- **A4:** inspects PR #173/current frontend and executes reproducible frontend checks.
- **A12:** independent reviewer for security, CI/test evidence, permissions and failure states.

A2 handles detailed visual-board work after A1 provides the brief; it can replace a completed session rather than increasing concurrency. A3 reviews system tokens once the reference direction exists. The 4-session limit refers to concurrent active work, not all roles that may participate sequentially.

## Tasks and outputs

### S0-01 — Freeze baseline and inspect in-flight work
Owner: A0
- Record the main SHA, open PRs, active branches, latest CI, current deployment workflow status, and feature status.
- Read root AGENTS, README, agent-system policy, previous governance and production checklist.
- Inspect PR #173's current base/head diff and test status, not only its title/body.
- Categorize features as EXISTING-VERIFIED, EXISTING-UNVERIFIED, PROTOTYPE, PLANNED or BLOCKED.
Output: audit table with source/PR/test links.

### S0-02 — Review frontend PR and prove build status
Owner: A4; reviewer A12
- Check current package manager and lockfile strategy; ensure reproducible dependency install.
- Run lint, typecheck if configured, production build and browser smoke test.
- Check the CSS issue noted in earlier static audit against the latest PR head. Fix only if reproducible and in a scoped implementation PR.
- Review desktop/mobile layout and accessibility, capture screenshots from running code, and inventory whether every control is functional/disabled/prototype.
Output: findings by severity, exact commands/results, screenshots, and disposition recommendation. Do not assume PR #173 should merge.

### S0-03 — Product requirements and provider decisions
Owner: A1
- Map journeys for assignment/deadline tracking, AI draft and artifact delivery, tasks/projects, automation, and developer diagrams.
- Define roles and their legitimate capabilities.
- Identify unresolved choices: first campus provider/API, WhatsApp integration path, storage, model providers/budgets, payment provider (later).
- Record privacy and academic-integrity constraints.
Output: owner-reviewable requirements, workflow map, page/role catalog and open decisions.

### S0-04 — Visual reference board and design system proposal
Owner: A2; consistency review A3; owner approves
- After requirements are known, research app shell/overview and AI workspace/task detail first.
- Provide 3–5 screenshot references per page cluster from at least two domains; include original links, source/date, adopt/reject notes, interaction-vs-visual distinction and license caveats.
- Recommend one coherent direction and map it to current tokens/components; do not deliver only a raw screenshot dump.
- Record owner approval status and revisions. No production UI build starts before approval.
Output: page-specific boards and design decision record.

### S0-05 — Shared contracts and security gap review
Owner: A0; consult A5/A12
- Draft identity/workspace, role/permission, task/run state, API error, artifact ownership, webhook and idempotency contracts.
- Label APIs as EXISTING or TARGET. Do not assume target route names already exist.
- Review known risks: single API key vs SaaS sessions, DEFAULT_USER/in-memory settings, resource/event isolation, WhatsApp inbound payload mapping, workflow runtime boundary.
Output: contract register and decision records with owners and states.

### S0-06 — Create prioritized GitHub work queue
Owner: A0; A12 signs off test/security plan
- Search existing Issues and PRs before creating work.
- Create one issue per reviewable vertical slice, set primary agent/reviewer, scope/file allowlist, dependencies, acceptance and test commands.
- Group issues in one GitHub Project. The Issue is the canonical work item; do not let Markdown status drift.
Output: Sprint 1 candidate tickets, dependency links, and blocked decisions.

## Sprint 0 exit criteria

- [ ] Main SHA, open PRs and latest CI results are recorded.
- [ ] PR #173 has source/diff/build/browser findings with evidence.
- [ ] Existing vs prototype vs target capability inventory is reviewed.
- [ ] User journeys, personas, roles and provider questions are documented.
- [ ] Reference direction for app shell and one representative page has owner decision.
- [ ] Auth/tenant, status/error, artifacts and integration contracts have named owners.
- [ ] GitHub Project and issue backlog have unique canonical work items.
- [ ] Every Sprint 1 ticket has dependencies, file owner, acceptance and test plan.
- [ ] A12 records blocker/high findings; A0 posts a truthful sprint review.
- [ ] Owner chooses the first integrated vertical slice.

Do not exit by merging UI because it looks good, starting every agent on “build all features”, claiming placeholder classes are a complete product, designing every route from one screenshot, or implementing an unauthorized generic campus scraper.
