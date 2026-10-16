# 12 — Initial Backlog for GitHub Issues

This is a starter queue to convert into real GitHub Issues and a GitHub Project. Do not track active state only in this Markdown file once Issues exist; the GitHub issue and Project become the source of truth. Check current open issues first and link/reuse existing tickets rather than creating duplicates.

## P0 — Sprint 0 (4 active agents)

| Suggested ID | Ticket | Owner | Dependencies | Exit condition |
|---|---|---|---|---|
| UTA-P0-01 | Audit current main, in-flight PRs, CI and release workflows | A0 | none | evidence-backed capability/PR matrix |
| UTA-P0-02 | Validate PR #173: dependency install, CSS, lint/build, browser screenshots | A2, reviewer A7 | P0-01 | reproducible findings and scoped fixes/issues |
| UTA-P0-03 | Document student workflows, persona/role matrix and open provider decisions | A1 | none | owner-reviewed requirements and decision list |
| UTA-P0-04 | Prepare screenshot reference boards for app shell/overview and AI workspace | A1, reviewer A2 | P0-03 | 3–5 sources per page cluster and owner decision |
| UTA-P0-05 | Draft auth/workspace/data/state/error contract decisions | A0; consult A3/A7 | P0-01 | contract register and ADR ready for review |
| UTA-P0-06 | Create priority GitHub Project and ticket graph | A0 | P0-01 to P0-05 | Sprint 1 tickets have owner/dependency/DoD |

## P1 — First implementation milestones

| Suggested ID | Ticket | Owner | Depends on |
|---|---|---|---|
| UTA-P1-01 | Define user/session/workspace schema and auth migration design | A3 | P0-05 |
| UTA-P1-02 | Enforce workspace tenant scoping for existing runs/settings/approvals/events | A3 + A7 | P1-01 |
| UTA-P1-03 | Connect reviewed frontend shell to real health/auth/API states | A2 | P0-02, P0-04, P1-01 |
| UTA-P1-04 | Add persisted workspace-scoped projects/tasks vertical slice | A4 + A3 | P1-02, P1-03 |
| UTA-P1-05 | Implement durable AI run-to-artifact journey using current safe runtime | A4 | P1-02, P1-04 |
| UTA-P1-06 | Complete WhatsApp inbound provider payload mapping and account link | A5 | P1-01 |
| UTA-P1-07 | Implement WhatsApp command → queued run → persisted artifact → result message | A5 + A4 | P1-05, P1-06 |
| UTA-P1-08 | Implement one authorized campus connector and assignment sync | A5 | P0-03, P1-01 |
| UTA-P1-09 | Design typed workflow schema/version contract | A6 + A0 | P1-05 |
| UTA-P1-10 | Implement one safe end-to-end workflow with run inspector | A6 | P1-09, P1-05 |
| UTA-P1-11 | GitHub least-privilege connection and repository selection | A6 | P1-01 |
| UTA-P1-12 | ERD + flowchart source/version/render/export vertical slice | A6 | P0-04, P1-03 |
| UTA-P1-13 | Independent security, accessibility and integrated journey suite | A7 | runs continuously; gates each PR |
| UTA-P1-14 | Usage ledger and quota contract before any paid plan | A0 + A3 + A4 | after usage requirements decision |

## Ticket creation rules

- Search GitHub Issues and Projects before making an issue.
- Replace suggested IDs with actual issue numbers after creation.
- Each issue has one primary agent, one independent reviewer, file ownership, dependencies, acceptance criteria, tests, permissions and evidence.
- Do not mark P1 tickets READY until dependencies are ACCEPTED/FROZEN.
- Maintain vertical acceptance scenarios. Prefer one integrated journey over five unrelated pages.
