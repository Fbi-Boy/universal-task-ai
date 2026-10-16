# 12 — Initial Backlog for GitHub Issues

This is the seed queue for the program. P0 work items below have been converted to canonical GitHub Issues; those issue numbers and links are authoritative. P1 remains a proposed seed queue and must be converted into Issues only after upstream findings, scope, contracts, dependencies, owner/reviewer roles, acceptance criteria, and test plans have been reviewed. Keep one issue per reviewable slice and search for duplicates before adding more.

## P0 — Sprint 0 (four concurrent sessions maximum)

| Seed ID (traceability only) | Ticket | Canonical GitHub issue | Owner role | Reviewer / dependency | Exit condition |
|---|---|---|---|---|---|
| UTA-P0-01 | Audit main, in-flight PRs, CI and release workflow | [#177](https://github.com/Fbi-Boy/universal-task-ai/issues/177) | A0 | A12; none | Evidence-backed capability/PR matrix |
| UTA-P0-02 | Validate PR #173: install, lockfile, CSS, lint/build, browser screenshots | [#178](https://github.com/Fbi-Boy/universal-task-ai/issues/178) | A4 | A12; #177 | Reproducible findings and scoped follow-up |
| UTA-P0-03 | Document student workflows, roles/personas and unresolved providers | [#179](https://github.com/Fbi-Boy/universal-task-ai/issues/179) | A1 | A0; none | Reviewed requirements and decision list |
| UTA-P0-04 | Prepare screenshot reference boards for shell/overview and AI workspace | [#180](https://github.com/Fbi-Boy/universal-task-ai/issues/180) | A2 | A3; #179 | 3–5 sources per cluster and owner decision |
| UTA-P0-05 | Draft identity/workspace, data/state/error contract decisions | [#181](https://github.com/Fbi-Boy/universal-task-ai/issues/181) | A0 | A5 + A12; #177 | Contract register and ADR ready for review |
| UTA-P0-06 | Verify/reuse or create GitHub Project and dependency-linked work queue | [#182](https://github.com/Fbi-Boy/universal-task-ai/issues/182) | A0 | A12; #177–#181 outputs | Verified Project URL and linked items, or explicit blocker |

A2 can start detailed board work once A1 requirements are clear. The 4-session limit applies concurrently; swap sessions as tasks are handed off rather than starting every role at once. The creation of these Issues is not proof that their work has started or their exit criteria are met. Issue #182 must stay blocked until Project visibility and a supported write path are verified; inspect/reuse a suitable existing Project before creating a new one.

## P1 — First implementation milestones (seed only; not yet canonical GitHub Issues)

| Suggested seed ID | Ticket | Owner role | Depends on |
|---|---|---|---|
| UTA-P1-01 | Define account/session/workspace schema and auth migration design | A5 | P0-05 |
| UTA-P1-02 | Enforce tenant scope for existing settings/runs/approvals/events/artifacts | A5 | P1-01 |
| UTA-P1-03 | Connect approved frontend shell to real auth/API/status states | A4 | P0-02, P0-04, P1-01 |
| UTA-P1-04 | Persist workspace-scoped projects and tasks vertical slice | A6 | P1-02, P1-03 |
| UTA-P1-05 | End-to-end AI run → reviewed artifact using current safe runtime | A7 | P1-02, P1-04 |
| UTA-P1-06 | Finish WhatsApp inbound mapping, account binding and webhook dedupe | A8 | P1-01 |
| UTA-P1-07 | WhatsApp command → queued run → saved artifact → safe result message | A8 | P1-05, P1-06 |
| UTA-P1-08 | Implement one authorized campus connector and assignment sync | A8 | P0-03, P1-01 |
| UTA-P1-09 | Freeze typed/versioned workflow schema | A9 | P1-05 |
| UTA-P1-10 | Execute one safe workflow with real run inspector | A9 | P1-09, P1-05 |
| UTA-P1-11 | GitHub least-privilege connection and explicit repository selection | A10 | P1-01 |
| UTA-P1-12 | ERD + flowchart source/version/render/export slice | A10 | P0-04, P1-03 |
| UTA-P1-13 | Independent security, accessibility and integrated journey suite | A12 | Gates every PR |
| UTA-P1-14 | Define usage ledger/quota contract before paid plan work | A0 + A5 + A7 | Product usage decision |

## Ticket rules
- Seed IDs are traceability tags only; the GitHub issue number/link is the canonical work-item ID once created.
- Every issue must have one primary role owner, independent reviewer, scope/file allowlist, dependencies, acceptance criteria, security/failure cases, test commands and evidence plan.
- Agent-role IDs (A0–A13) are not GitHub usernames. Do not guess account mappings or bulk-assign users.
- Do not mark P1 work READY before required contracts and upstream slices are ACCEPTED/FROZEN.
- Favor one integrated user journey over multiple unrelated mock pages.
- Do not report completion until the acceptance criteria and evidence in the ticket are reviewed.
