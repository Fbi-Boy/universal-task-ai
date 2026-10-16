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

## Current iteration
- Sprint: 0 — Program and design baseline.
- Objective: verify what exists; lock contracts and design decision process; create prioritized, dependency-safe tickets.
- Implementation permission: no broad feature coding until relevant tickets pass G0/G1/G2.
- Owner approvals required: product scope, reference direction for representative pages, auth/session product choice, campus connector pilot, and any production action.

## Sprint 0 GitHub execution queue
Snapshot recorded on 16 October 2026 against main SHA `0f4151c067815106d6600f47bab403e5e674c64c`; refresh the SHA and PR/check state before work starts.

| Canonical issue | Work item | Role owner / reviewer | Status at setup |
|---|---|---|---|
| [#177 — repository baseline audit](https://github.com/Fbi-Boy/universal-task-ai/issues/177) | Evidence-backed inventory of main, open PRs, CI and release status | A0 / A12 | NOT STARTED |
| [#178 — frontend PR #173 validation](https://github.com/Fbi-Boy/universal-task-ai/issues/178) | Reproduce install/lint/build/browser findings on current PR head | A4 / A12 | NOT STARTED; depends on #177 |
| [#179 — student workflows and decisions](https://github.com/Fbi-Boy/universal-task-ai/issues/179) | Define student journeys, roles, provider and product decisions | A1 / A0 | NOT STARTED |
| [#180 — visual reference boards](https://github.com/Fbi-Boy/universal-task-ai/issues/180) | Audit/reuse existing board and complete page-specific references | A2 / A3 | NOT STARTED; depends on #179 |
| [#181 — shared contract review](https://github.com/Fbi-Boy/universal-task-ai/issues/181) | Draft evidence-backed auth/workspace/state/error/integration contracts | A0 / A12 (consult A5) | NOT STARTED; depends on #177 |
| [#182 — Project board verification/setup](https://github.com/Fbi-Boy/universal-task-ai/issues/182) | Verify/reuse a suitable board or create one only if absent; verify canonical issue links | A0 / A12 | BLOCKED: Project visibility/write capability not verified |

Important operating notes:
- Issue numbers above are the canonical work-item IDs. Seed IDs like `UTA-P0-01` are traceability tags only.
- An issue being open means only that it is not closed; it does **not** mean its work has started or been accepted. At setup, #177–#181 are NOT STARTED and #182 is BLOCKED.
- A0–A13 are agent-role identifiers, not verified GitHub usernames. No GitHub assignees have been guessed or assigned.
- The available GitHub connection could create and read Issues but did not expose a Projects write operation. Project existence/visibility could not be conclusively verified. No Project URL is recorded and no claim is made that the issues have been added to a Project. Before creating a new board, inspect and reuse a suitable existing one if present; see #182.
- Creating this issue queue is program setup, not evidence that the audit, product research, design review, contract review, or any product implementation has completed.

## Status legend
- NOT STARTED — no work or evidence exists.
- IN PROGRESS — scoped work underway with issue/branch.
- BLOCKED — named missing decision/dependency/environment prevents progress.
- IN REVIEW — PR exists and review/evidence is pending.
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
