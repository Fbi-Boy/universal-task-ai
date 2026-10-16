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
- Seed backlog: docs/agent-program/12_INITIAL_BACKLOG.md; convert unique tickets to real GitHub Issues and a Project before implementation starts.
- Active concurrent AI target: 4 during Sprint 0; 6 during normal development; practical cap 7.
- High-priority risks: identity/tenant model, frontend prototype-vs-live boundary, WhatsApp inbound mapping, provider-specific campus auth, design consistency and parallel agent conflicts.

## Current iteration
- Sprint: 0 — Program and design baseline.
- Objective: verify what exists; lock contracts and design decision process; create prioritized, dependency-safe tickets.
- Implementation permission: no broad feature coding until relevant tickets pass G0/G1/G2.
- Owner approvals required: product scope, reference direction for representative pages, auth/session product choice, campus connector pilot, and any production action.

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
2. active PRs and latest-head CI/security status;
3. accepted work with issue/PR/commit links;
4. blocked work and the exact action needed;
5. contract/ADR and design approval status;
6. risk changes supported by evidence;
7. next milestone, dependency tickets and assigned agents;
8. tests not run and known limitations.

Do not write completion percentages unless an explicit metric formula and evidence source are defined. Do not report that this program folder is in main until its PR is actually merged.
