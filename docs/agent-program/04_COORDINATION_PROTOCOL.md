# 04 — Agent Coordination Protocol

## GitHub is the shared memory

All active agents must use the same repository and agreed GitHub Project. Chat prompts are ephemeral; the authoritative status and decision must be persisted.

Use:
- **GitHub Project** for active ticket/status/dependency views.
- **GitHub Issues** for ownership, acceptance criteria, estimate, dependencies, test plan and blockers.
- **Pull Requests** for implementation, screenshots, evidence, reviewer comments and CI.
- **docs/agent-program/** for work program and contract index.
- **docs/agent-system/** for current governance prompts, broader product blueprint and visual references.
- **ADRs and contract files** for shared architecture/API/data/status decisions.

Before creating a duplicate issue, search the project and repository. One real work item should have one canonical issue ID.

## Ticket lifecycle

READY → IN_PROGRESS → BLOCKED (when needed) → REVIEW → ACCEPTED → DONE.

- READY: dependency, scope, owner, acceptance, file ownership, contract and design approval are present.
- IN_PROGRESS: agent has assigned branch and is actively implementing.
- BLOCKED: a real dependency/provider/owner decision/test environment is missing; report reason and requested action.
- REVIEW: implementation is ready, PR is open and local self-review is done.
- ACCEPTED: independent A7 findings resolved, tests/CI on current PR head pass and A0 accepts integration.
- DONE: merged according to repository policy and relevant documentation/state updated.

Do not skip states just to show progress. If only docs/code were written but tests are not run, it cannot pass the applicable test gate.

## Required handoff packet

Each agent must report:
1. Issue ID, role, branch and PR link.
2. Base commit SHA and current PR HEAD SHA.
3. Paths modified and the reason for each.
4. Contract/ADR/schema affected, with new links.
5. Acceptance criteria: PASS / FAIL / NOT RUN, each with evidence.
6. Exact commands executed and results; distinguish local from CI.
7. UI screenshot/reference comparison and viewport if UI changed.
8. Security, tenant isolation, permission, retry/idempotency and failure cases reviewed as applicable.
9. Known bugs, limitations, blockers and unresolved decisions.
10. Recommended next owner/ticket and dependencies.

## Parallel working rules

- A0 publishes tickets and file ownership before work begins.
- Two agents may work in parallel only if contracts are stable and write paths do not overlap.
- All shared types/API/schema/theme/migration files have a single owner per batch.
- A dependent ticket cannot start against a moving contract without acknowledging the change.
- Agents must not edit each other's branch or resolve architectural conflict by copying conflicting code together.
- Conflicts go to A0 with options, impact, evidence and recommendation; high-risk product/privacy/design decisions go to the human owner.

## Branch / PR policy

- Use names such as feat/UTA-123-task-inbox, fix/UTA-124-webhook-dedupe, docs/UTA-125-program-charter.
- One ticket or tightly coupled slice per PR.
- PR description includes purpose, scope in/out, screenshots, API/data/migration changes, tests actually run, security considerations, rollout/rollback and limitations.
- No direct commit to main as ordinary work; no force-push of shared branches.
- Review CI against the latest PR HEAD.
- Merge method follows repository policy and owner approval. PR author should not be the only reviewer on security-sensitive changes.
- Never put API tokens, cookies, student credentials, real assignment content or private data in issues, fixtures or screenshots.

## Coordination cadence

At the start of a work session, A0 posts a short plan: milestone, issues unlocked, agent owner, blocked dependencies and gate required.

When a ticket is ready for review, the implementer sends the required handoff packet and adds A7 as reviewer.

At the end of a sprint, A0 updates program state and posts:
- accepted items with merge links;
- issues not accepted and why;
- contract/design decisions;
- next dependencies;
- risks and human decisions needed.

Do not send “still working” messages as substitute for evidence. Do not claim a background process will finish later; agents must either do the work in the active session or leave a truthful BLOCKED/PARTIAL report.
