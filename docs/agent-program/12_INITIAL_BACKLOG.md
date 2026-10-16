# 12 — Initial Backlog for GitHub Issues

This is a seed queue to convert into GitHub Issues and one Project. The Project/Issues become the active status source of truth after setup. Search current Issues and PRs first; link/reuse existing tickets rather than creating duplicates.

## P0 — Sprint 0 (four concurrent sessions maximum)

| Suggested ID | Ticket | Owner | Reviewer / dependency | Exit condition |
|---|---|---|---|---|
| UTA-P0-01 | Audit main, in-flight PRs, CI and release workflow | A0 | A12; none | evidence-backed capability/PR matrix |
| UTA-P0-02 | Validate PR #173: install, lockfile, CSS, lint/build, browser screenshots | A4 | A12; P0-01 | reproducible findings and scoped follow-up |
| UTA-P0-03 | Document student workflows, roles/personas and unresolved providers | A1 | A0; none | reviewed requirements and decision list |
| UTA-P0-04 | Prepare screenshot reference boards for shell/overview and AI workspace | A2 | A3; P0-03 | 3–5 sources per cluster and owner decision |
| UTA-P0-05 | Draft identity/workspace, data/state/error contract decisions | A0 | A5 + A12; P0-01 | contract register and ADR ready for review |
| UTA-P0-06 | Create priority GitHub Project and dependency-linked work tickets | A0 | A12; P0-01..P0-05 | Sprint 1 tickets have owner/dependencies/DoD |

A2 can start once A1 requirements are clear. The 4-session limit applies concurrently; swap sessions as tasks are handed off rather than starting every role at once.

## P1 — First implementation milestones

| Suggested ID | Ticket | Owner | Depends on |
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
| UTA-P1-13 | Independent security, accessibility and integrated journey suite | A12 | gates every PR |
| UTA-P1-14 | Define usage ledger/quota contract before paid plan work | A0 + A5 + A7 | product usage decision |

## Ticket rules
- Suggested IDs are placeholders. Replace them with real GitHub issue numbers.
- Every issue has one primary owner, independent reviewer, allowed file paths, dependencies, acceptance criteria, security/failure cases, test commands and evidence plan.
- Do not mark P1 work READY before required contracts and upstream slices are ACCEPTED/FROZEN.
- Favor one integrated user journey over multiple unrelated mock pages.
