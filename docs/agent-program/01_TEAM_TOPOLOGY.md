# 01 — Team Topology: How Many AI Agents?

## Recommendation

Do not run 14 independent agents in parallel. Start with **4 active agents during Sprint 0**, then move to **6 active agents during implementation**. Keep **7 concurrent agents as the practical maximum** until coordination is measurably reliable. The number refers to active work sessions, not all prompt profiles available in the repository.

The recommended steady-state team has these 8 role profiles. A role can be activated when needed; the team cap still applies.

| ID | Role | Owns | Must not do |
|---|---|---|---|
| A0 | Program Orchestrator / Chief Architect | issues, contracts, ADRs, dependencies, assignments, integration, program status | secretly change feature code while acting as reviewer of that same change; approve own design |
| A1 | Product & Design Research | research, user flows, requirements, visual reference boards, evidence links | production UI implementation before owner design approval |
| A2 | Frontend & Design System | tokens, shared shell/components, Next.js routes, API client/UI states | invent APIs, use fake live metrics, bypass server auth |
| A3 | Identity & Backend Platform | accounts, sessions, workspace/RBAC, database, API schemas and tenant isolation | own all domain logic or let IDs from request bodies define access |
| A4 | Student Tasks & AI Workspace | projects/tasks/backlog, conversations, runs, approvals, artifacts, model/runtime integration | bypass existing safe tool boundary or claim unsupported work succeeded |
| A5 | Integrations Engineer | WhatsApp, notifications, campus connector pilot, source sync/checkpoints | assume all LMS platforms are the same or automate unauthorized official actions |
| A6 | Automation & Developer Studio | workflow schema/builder/runtime, GitHub, ERD/DFD/flowchart/UML increments | treat a visual canvas or current regex validator as a safe, complete runtime |
| A7 | Independent QA, Security & Release Readiness | tests, threat review, browser/a11y evidence, dependency risk, readiness and release checklist | review only from implementer claims, or waive product-owner release approval |

DevOps/payment/licensing research is a specialist capability called on by A0 when the phase needs it; it does not require a dedicated always-running agent in the first phase. If a billing payment integration, production deployment or a new runtime system becomes active, split that responsibility into a dedicated temporary specialist and reduce other concurrency to stay under the cap.

## Active capacity by phase

### Sprint 0: 4 active roles maximum
- A0: current repo/PR/architecture audit and work breakdown.
- A1: requirements, visual reference research and page catalog.
- A2: inspect frontend PR and validate shared design system; no production feature build.
- A7: independent repo/security/test gap review.

A3–A6 remain inactive until contracts and dependency ownership are clear. This prevents premature parallel implementation.

### Normal implementation: 6 active agents
Always include A0 and A7 review capacity; select no more than four domain workers from A2–A6 for the tickets whose dependencies are satisfied. Asynchronous, independent research can be performed by A1 without creating overlapping code edits, but total active sessions should remain capped at six unless A0 explicitly records a reason.

### Hard practical cap: 7 active
Use a seventh slot only when every worker has independent paths/contracts and one integrator is available. If merge conflicts, duplicate API contracts, inconsistent styles, or unresolved handoffs increase, reduce parallelism instead of adding agents.

## Reporting lines

Product Owner → A0 → domain owner(s) → A7 independent review → A0 integration decision → owner approval where required.

A0 cannot assign two agents the same file ownership in the same working window. Shared files (root AGENTS, API schema, design tokens, shared navigation, migrations, workflow state machine) have one named owner per ticket. Parallel work can touch those files only after an explicitly approved contract/change window.

## When to create a new agent role

Create a new specialist only if:
1. It owns a substantial independent knowledge area.
2. It has a separate deliverable, measurable acceptance criteria and test strategy.
3. Existing roles cannot reasonably cover it without exceeding capacity.
4. A0 has defined dependencies and file ownership.
5. The work is important enough to justify the coordination cost.

Do not spawn an agent for a tiny subtask; use a subtask under the appropriate domain issue.
