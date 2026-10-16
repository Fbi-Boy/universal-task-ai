# 09 — Sprint 0 Runbook: What Happens First

## Goal

Create a trustworthy baseline, not new features. At the end of Sprint 0 the team should agree on what exists, what is prototype-only, which contracts need decisions, which designs are approved, and the next small tickets with dependencies.

## Team capacity: four active agent roles

- A0 Program Orchestrator — owns this runbook, current source/PR audit, ticket plan and decision log.
- A1 Product & Design Research — checks student journeys, role/page catalog and source-backed visual references.
- A2 Frontend & Design System — reviews PR #173/current frontend implementation, identifies concrete fixes, checks build, tokens and responsive design.
- A7 QA/Security/Release — independently reviews current CI/security, tests, permissions, failure states and risky assumptions.

Do not activate implementation agents A3–A6 until the appropriate contract/ticket is READY. This is deliberate, not idle work.

## Day/task sequence (finish by evidence, not by calendar)

### S0-01 — Freeze baseline commit and inspect in-flight work
Owner: A0  
Actions:
- Check main SHA, working tree assumptions, open PRs, most recent CI runs and active feature branches.
- Read README, AGENTS, agent-system docs, roadmap and deployment/production checklist.
- Inspect PR #173 and its base/head diff, not just the title/body.
- Label each capability EXISTING-VERIFIED, EXISTING-UNVERIFIED, PROTOTYPE, PLANNED, or BLOCKED.
Output: audit table with file/PR/test evidence.

### S0-02 — Frontend PR verification
Owner: A2; reviewer A7  
Actions:
- Install with reproducible package-manager/lockfile setup.
- Run lint, typecheck if configured, production build and browser smoke test.
- Inspect the apparent CSS syntax issue identified in the previous audit, verify whether it still exists, and fix only in a scoped feature PR.
- Test desktop and mobile layout; capture screenshots from the running app.
- Inventory every UI control: functional, disabled with a reason, or explicitly labeled prototype.
Output: finding list with severity and screenshots. This is review work; do not assume the PR should merge.

### S0-03 — Requirements and persona map
Owner: A1  
Actions:
- Define core user jobs and prioritized personas.
- Map assignment detection, deadline reminder, task execution, artifact delivery, workflow building and IT diagram creation.
- Mark provider-dependent decisions such as exact LMS, WhatsApp provider path and payment provider as OPEN decisions.
- Check user privacy and academic integrity boundaries.
Output: requirements, user flows, initial screen/role matrix, open decision list.

### S0-04 — Visual design baseline
Owner: A1; consistency reviewer A2; product owner approves  
Actions:
- Select 2 representative screen clusters first: app shell/overview and AI workspace/task detail.
- For each, prepare 3–5 screenshot references from at least two domains, direct source link, adopt/reject notes, layout comparison and proposed token mapping.
- Do not ask the owner to approve a raw screenshot dump; provide one recommendation and alternatives/trade-offs.
- Record approval status and comments.
Output: page-specific board, shared design-system proposal, owner decision record.

### S0-05 — Contracts and security gap review
Owner: A0; reviewers A3/A7 are consulted when activated  
Actions:
- Draft identity/workspace/role contract, task/run status vocabulary, error format, event/idempotency semantics, artifact ownership and integration connection scope.
- Inspect existing APIs and stores; mark each proposed endpoint as EXISTING or TARGET.
- Make a risk register entry for global API-key/local mode vs SaaS account sessions, in-memory settings, current run/event scoping and WhatsApp inbound mapping.
Output: contract register with ownership and status DRAFT/REVIEW/FROZEN.

### S0-06 — Backlog and readiness review
Owner: A0; A7 signs off test/risks  
Actions:
- Create or update GitHub Issues for the tickets in INITIAL_BACKLOG.
- Make one issue per reviewable vertical slice. Connect blockers/dependencies.
- Assign primary agent, reviewer, allowed paths, acceptance criteria and test commands.
- Select the first user-visible end-to-end slice to deliver.
Output: Sprint 1 READY tickets plus blocked/open decisions.
  
## Sprint 0 exit criteria

- [ ] Main SHA, open PRs, and CI status are recorded.
- [ ] PR #173 findings use source/diff/test evidence, not assumptions.
- [ ] Existing vs prototype vs target capability inventory is reviewed.
- [ ] Product roles and main student workflows are documented.
- [ ] Reference board has owner decision for app shell and at least one representative page.
- [ ] Auth/tenant, task/run states, artifact ownership and integration contracts have named owners.
- [ ] Initial backlog exists in GitHub Issues/Project; no duplicate ticket for the same work.
- [ ] Every Sprint 1 ticket has dependency, file owner, acceptance and test plan.
- [ ] A7 records unresolved blocker/high risks and makes a recommendation.
- [ ] A0 posts a sprint review report; owner agrees on next milestone.

## Do not exit Sprint 0 by

- Merging a UI PR only because the screenshot looks good.
- Starting every agent on “build all features”.
- Marking unimplemented modules complete because classes or placeholders exist.
- Designing the full site from one Dribbble shot.
- Adding billing/payment or generic campus scraping before source/consent/terms are understood.
