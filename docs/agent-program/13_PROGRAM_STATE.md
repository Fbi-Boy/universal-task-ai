# 13 — Program State & Sprint Log

> This file is a snapshot of what is known from the repository audit; it is not live telemetry. A0 must update it after reviewing current GitHub data and after each sprint. Never treat a planned or historical capability as currently working without re-verification.

## Baseline
- Repository: Fbi-Boy/universal-task-ai
- Default branch: main
- Program workbook PR: [#175 — coordinated AI agent program workbook](https://github.com/Fbi-Boy/universal-task-ai/pull/175), merged 16 October 2026.
- Existing governance folder: docs/agent-system/
- New operational program folder: docs/agent-program/
- Program folder status: ACTIVE IN MAIN. Initial merge commit: d594a6c9c32d824b4c6c29add80dca4c558a9ac2. This is the documentation baseline, not a claim that any planned product feature is implemented. Treat this document as a snapshot that must be refreshed against GitHub.
- Product milestone: Sprint 0, repository/PR/design/contracts/backlog audit.
- Seed backlog: docs/agent-program/12_INITIAL_BACKLOG.md. P0 work items now have canonical GitHub Issues; P1 remains a seed queue and must be converted only after upstream scope/contracts/dependencies are reviewed.
- Active concurrent AI target: 4 during Sprint 0; 6 during normal development; practical cap 7.
- High-priority risks: identity/tenant model, frontend prototype-vs-live boundary, WhatsApp inbound mapping, provider-specific campus auth, design consistency and parallel agent conflicts.

## Last source/CI audit snapshot

- Audit report: [Sprint 0 Repository Baseline Audit](audits/SPRINT_0_BASELINE.md), being delivered in [PR #183](https://github.com/Fbi-Boy/universal-task-ai/pull/183).
- Audited `main` SHA: [`0f4151c067815106d6600f47bab403e5e674c64c`](https://github.com/Fbi-Boy/universal-task-ai/commit/0f4151c067815106d6600f47bab403e5e674c64c) on 16 October 2026.
- On that exact SHA, [CI](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38912071438), [Integration and Security](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38912071471), and [Container Release](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38912071900) completed successfully.
- Container Release success means an immutable image was built/pushed; it does **not** mean production deployment occurred. Production rollout remains unverified/incomplete.
- PR #173 is still a frontend draft, not in `main`; its last recorded [Frontend CI](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38772286887) failed production build due an unclosed bracket in `frontend/app/globals.css`. See the audit report for exact evidence and the lockfile/browser-test gaps.
- PR #165 remains open and non-mergeable, with an old base. It may overlap with merged PR #168; its diff is not identical, so compare file-by-file before deciding whether it is superseded. Do not merge it as-is.
- Source-verified product gaps include global API-key authentication instead of user/workspace sessions, in-memory settings attached to `DEFAULT_USER`, unfinished WhatsApp inbound payload mapping, and no verified campus/LMS connector or durable visual-workflow API slice on the audited main tree.
- GitHub Projects existence/visibility and write capability remain unverified. Issue #182 is blocked; no Project URL is recorded and no Project creation/linkage is claimed.
- The audit is awaiting independent A12 review. Source inspection and CI evidence are not a substitute for browser checks, provider end-to-end tests or a production deployment.

## Open documentation PR status — 16 October 2026

| PR | Exact head checked | Latest recorded checks | Review / merge status |
|---|---|---|---|
| [#183 — baseline audit and issue queue](https://github.com/Fbi-Boy/universal-task-ai/pull/183) | See live PR head; this Program State document changes that PR | Recheck CI and Integration/Security on the latest PR head before merge; do not use a previous-head result as current | Open; independent A12 review pending |
| [#184 — product requirements draft](https://github.com/Fbi-Boy/universal-task-ai/pull/184) | `e1267861950384effc9d3e7170e490918b1fff58` | CI [run 38914939641](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38914939641) PASS; Integration/Security [run 38914939977](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38914939977) PASS | Open; no PR reviews recorded; owner product decisions and approval pending |
| [#185 — visual reference review](https://github.com/Fbi-Boy/universal-task-ai/pull/185) | `358a3adb8f4c2d4bfaee8c71b13fb8fd1400b1c5` | CI [run 38916027636](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38916027636) PASS; Integration/Security [run 38916028728](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38916028728) PASS | Open; no PR reviews recorded; visual direction is PROPOSED, not owner-approved |

A passing CI/security run is necessary but does not equal independent review, product-owner approval, acceptance, merge or production release. Refresh PR #183's run status after this change and do not mark any of these PRs accepted from checks alone.

## Current iteration
- Sprint: 0 — Program and design baseline.
- Objective: verify what exists; lock contracts and design decision process; create prioritized, dependency-safe tickets.
- Implementation permission: no broad feature coding until relevant tickets pass G0/G1/G2.
- Owner approvals required: product scope, reference direction for representative pages, auth/session product choice, campus connector pilot, and any production action.

## Sprint 0 GitHub execution queue

Snapshot recorded on 16 October 2026 against main SHA `0f4151c067815106d6600f47bab403e5e674c64c`; refresh the SHA and PR/check state before work starts.

| Canonical issue | Work item | Role owner / reviewer | Status at audit update |
|---|---|---|---|
| [#177 — repository baseline audit](https://github.com/Fbi-Boy/universal-task-ai/issues/177) | Evidence-backed inventory of main, open PRs, CI and release status | A0 / A12 | A0 coordinator review recorded; PR #183 CI/security passed on latest recorded head before this state update; A12 independent review pending and reviewer identity not mapped |
| [#178 — frontend PR #173 validation](https://github.com/Fbi-Boy/universal-task-ai/issues/178) | Reproduce install/lint/build/browser findings on current PR head | A4 / A12 | NOT STARTED; acceptance of #177 and current-head rerun still needed |
| [#179 — student workflows and decisions](https://github.com/Fbi-Boy/universal-task-ai/issues/179) | Define student journeys, roles, provider and product decisions | A1 / A0 | IN REVIEW via [PR #184](https://github.com/Fbi-Boy/universal-task-ai/pull/184); A0 review recorded; CI/security pass on head `e1267861950384effc9d3e7170e490918b1fff58`; A12 and owner decision pending |
| [#180 — visual reference boards](https://github.com/Fbi-Boy/universal-task-ai/issues/180) | Audit/reuse existing board and complete page-specific references | A2 / A3 | IN REVIEW via [PR #185](https://github.com/Fbi-Boy/universal-task-ai/pull/185); A0 alignment review recorded; CI/security pass on head `358a3adb8f4c2d4bfaee8c71b13fb8fd1400b1c5`; A3 and owner approval pending |
| [#181 — shared contract review](https://github.com/Fbi-Boy/universal-task-ai/issues/181) | Draft evidence-backed auth/workspace/state/error/integration contracts | A0 / A12 (consult A5) | NOT STARTED; depends on #177 |
| [#182 — Project board verification/setup](https://github.com/Fbi-Boy/universal-task-ai/issues/182) | Verify/reuse a suitable board or create one only if absent; verify canonical issue links | A0 / A12 | BLOCKED: Project visibility/write capability not verified |

Important operating notes:
- Issue numbers above are the canonical work-item IDs. Seed IDs like `UTA-P0-01` are traceability tags only.
- An issue being open means only that it is not closed; it does **not** mean its work has started or been accepted.
- A0–A13 are agent-role identifiers, not verified GitHub usernames. No GitHub assignees have been guessed or assigned.
- The available GitHub connection could create and read Issues but did not expose a Projects write operation. Project existence/visibility could not be conclusively verified. No Project URL is recorded and no claim is made that the issues have been added to a Project. Before creating a new board, inspect and reuse a suitable existing one if present; see #182.
- Creating this issue queue is program setup, not evidence that product research, design approval, contract review, or product implementation has completed.

## Status legend
- NOT STARTED — no work or evidence exists.
- IN PROGRESS — scoped work underway with issue/branch.
- BLOCKED — named missing decision/dependency/environment prevents progress.
- IN REVIEW — PR exists, with acceptance/evidence/review pending.
- ACCEPTED — independent review and required evidence complete.
- DONE — merged; code/docs/status verified.
- NOT RUN — check was not executed; never equal to PASS.

## Update protocol

After every material sprint decision/merge, A0 must update:
1. last audited main SHA/date;
2. active PRs and latest CI/security status on the latest heads;
3. accepted work with issue/PR/commit links;
4. blocked work and the exact action needed;
5. contract/ADR and design approval status;
6. risk changes supported by evidence;
7. next milestone, dependency tickets and assigned agents;
8. tests not run and known limitations.

Do not write completion percentages unless an explicit metric formula and evidence source are defined. Do not report that this program folder is in main until its PR is actually merged.
