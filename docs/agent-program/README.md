# Universal Task AI — Agent Program Workbook

This folder is the operational handbook for using multiple AI agents as one coordinated engineering team. It complements, rather than replaces, repository policy in AGENTS.md and the technical/product rules in docs/agent-system/.

## Start here — mandatory reading order

1. Root [AGENTS.md](../../AGENTS.md) — mandatory rules for every contributor.
2. This folder's [Program Charter](00_PROGRAM_CHARTER.md) — scope, authority, deliverables and operating assumptions.
3. [Team Topology](01_TEAM_TOPOLOGY.md) — how many agents to run, role ownership and concurrency.
4. [Workstreams & WBS](02_WORKSTREAMS_AND_WBS.md) — work packages and boundaries.
5. [Dependency Map](03_DEPENDENCY_MAP.md) — what must be completed before parallel work starts.
6. [Coordination Protocol](04_COORDINATION_PROTOCOL.md) — issue/branch/PR handoffs and shared source of truth.
7. [Ticket Packet](05_TICKET_PACKET_TEMPLATE.md) — required format for every assignment.
8. [Design Research & Approval](06_DESIGN_RESEARCH_AND_APPROVAL.md) — reference images, design approval and visual QA.
9. [Contract Register](07_SHARED_CONTRACT_REGISTER.md) — shared API/data/state contracts.
10. [Quality Gates & DoD](08_QUALITY_GATES_AND_DOD.md) — pass/fail requirements.
11. [Sprint 0 Runbook](09_SPRINT_0_RUNBOOK.md) — immediate next actions.
12. [Prompt Library](10_AGENT_PROMPTS.md) — reusable role prompts.
13. [Risk Register](11_RISK_REGISTER.md) — known cross-cutting risks.
14. [Initial Backlog](12_INITIAL_BACKLOG.md) — first epics/tickets and dependencies.
15. [Program State](13_PROGRAM_STATE.md) — baseline and update rules.
16. [Owner Decision Packet](14_OWNER_DECISION_PACKET.md) — unresolved Sprint 0 decisions, recommended defaults, and exact gates blocking Sprint 1.

## Recommended operating model

Use GitHub Issues + one GitHub Project as the system of record. Keep architecture decisions, design approvals, contracts, and delivery evidence in versioned files here. Chat messages are discussion, not the authoritative record. A0 maintains the project state; specialists work only assigned issues; independent QA reviews the implementation.

Recommended starting capacity: **4 active AI agents for Sprint 0**. For normal feature delivery, use **6 active agents as the default, with 7 as the practical cap**. Do not launch every specialist at once. Unused roles are on-demand capacities, not idle bots.

## Current milestone

Sprint 0 is repository/PR/architecture/design audit only. Do not begin a broad rollout of features until the current code, in-flight PRs, API/data contracts, visual system, dependencies, and prioritized backlog are reviewed.

## Important truthfulness rule

This folder is a work program, not implementation proof. A planned module is not “done” until code, contract, tests and review evidence exist. Update Program State after a material decision or completed gate; never make up percentages or statuses.
