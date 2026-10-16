# Sprint 0 — Repository Baseline Audit

**Audit date:** 16 October 2026  
**Repository:** [Fbi-Boy/universal-task-ai](https://github.com/Fbi-Boy/universal-task-ai)  
**Audited `main` commit:** [`0f4151c067815106d6600f47bab403e5e674c64c`](https://github.com/Fbi-Boy/universal-task-ai/commit/0f4151c067815106d6600f47bab403e5e674c64c)  
**Related ticket:** [#177 — Audit repository baseline, open PRs, CI and release workflow](https://github.com/Fbi-Boy/universal-task-ai/issues/177)  
**Evidence type:** source inspection + GitHub PR/workflow metadata. No local product test run, live browser session, or production-host access was performed for this audit.

## 1. Executive summary

The current `main` branch has a useful Python/FastAPI AI task runtime, an API-key authentication boundary, tool/runtime policy controls, approvals, audit/run state stores, an existing backend-served web UI, and passing Python CI plus integration/security workflows on the audited commit.

**This is not yet evidence of a multi-user student SaaS or production deployment.** Current auth is based on one configured bearer API key rather than user sessions/workspace membership. Settings are attached to a fixed `DEFAULT_USER` and held in an in-memory store. WhatsApp inbound authentication checks the signature but the provider payload decoder deliberately raises `NotImplementedError`. A campus/LMS connector, durable project/task workspace, full workflow-definition API, and subscription/usage service were not found in the audited `main` source tree.

PR #173 is a **draft frontend prototype**, not part of `main`. Its most recent recorded Frontend CI run fails during production build because `frontend/app/globals.css` has an unclosed bracket. Backend CI and Integration/Security passing do not compensate for this separate frontend failure.

## 2. Main branch CI and release evidence

All three workflow runs below are for the exact audited `main` SHA `0f4151c067815106d6600f47bab403e5e674c64c`.

| Check | Result | Evidence |
|---|---|---|
| CI — full Python test suite and compile check | PASS | [Run 38912071438](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38912071438) |
| Integration and Security — integration/security tests, regression suite, compile and dependency audit | PASS | [Run 38912071471](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38912071471) |
| Container Release — build/push immutable commit image and publish digest | PASS | [Run 38912071900](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38912071900) |

The container release run proves that the image pipeline succeeded for this commit. It **does not** prove that the image was deployed to a production server. The repository's [production deployment instructions](https://github.com/Fbi-Boy/universal-task-ai/blob/main/docs/operations/PRODUCTION_DEPLOYMENT.md) say a real rollout depends on configured protected-environment secrets and a deployment against the operator's infrastructure. [README status](https://github.com/Fbi-Boy/universal-task-ai/blob/main/README.md) likewise describes real production rollout as incomplete.

These workflow results are source/repository validation, not proof of browser usability, external provider credentials, live integrations or real production persistence.

## 3. Open pull requests at audit time

| PR | Observed state | Evidence-based disposition |
|---|---|---|
| [#165 — safely auto-route explicit arithmetic tasks](https://github.com/Fbi-Boy/universal-task-ai/pull/165) | Open, not draft, GitHub reports non-mergeable. Head `7c46a15e2ca71ee3425dea45f4c60e4928c6be47`; recorded base SHA `ebc23bd64ac95ad8c1443b94a10d49abcb8e5c75`. | Suspected superseded/stale candidate: it has the same title and changed-file/addition/deletion counts as merged [#168](https://github.com/Fbi-Boy/universal-task-ai/pull/168), which added the same narrow arithmetic-routing feature. The diffs are **not byte-identical**, so compare file-by-file before deciding whether to close #165. Do not merge it as-is; current `main` already has `auto_route_tools` handling in the task API. |
| [#173 — premium dashboard and visual workflow builder](https://github.com/Fbi-Boy/universal-task-ai/pull/173) | Open draft; head `248ad56257ffb4bc053f65d9496fed860b62e89b`. Frontend CI failure recorded 15 October 2026. | Changes requested before considering merge. Re-run on a current merge ref after the fix because `main` advanced after the recorded failing run. |
| [#183 — Sprint 0 issue/backlog documentation](https://github.com/Fbi-Boy/universal-task-ai/pull/183) | Open; initial head `b6f69d271efaed4ef877d234de92380dcb6f2da4` had CI and Integration/Security pass. | Documentation-only queue update. Re-check CI on its newest head after adding this audit; independent review and merge are still required. |

### PR #173: reproducible frontend blocker

The recorded [Frontend CI run 38772286887](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38772286887) reports dependency installation PASS and lint PASS, but production build FAIL. The [build log](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38772286887) identifies:

```
./app/globals.css:3:176
Syntax error: frontend/app/globals.css Unclosed bracket
```

The failing CSS declaration is the `--shadow` value: `rgba(37,35,84,.035}` closes the CSS block without first closing `rgba(` with `)`. This needs a scoped fix and a fresh build, not a waiver of CI.

Other follow-ups:
- The changed-file list for PR #173 contains no `frontend/package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`; its CI uses `npm install`. Add and use an agreed lockfile/install strategy so builds are reproducible.
- Frontend CI only runs install, lint and production build; the PR description's browser smoke/screenshot review remains NOT RUN in this audit.
- The frontend source contains illustrative metrics/activity and client-only workflow draft interactions; the PR's own [README](https://github.com/Fbi-Boy/universal-task-ai/blob/feat/premium-dashboard-frontend/frontend/README.md) states task submission, workflow persistence, drag/drop and real workflow execution are not connected to backend APIs.
- The current `main` branch does not contain this Next.js app because PR #173 has not merged.

## 4. Capability inventory

Status is scoped to the audited commit/source. "Verified" means the code path exists and/or repository checks pass; it does not claim that a configured external provider or a live production account was exercised.

| Area | Status | Evidence / consequence |
|---|---|---|
| FastAPI task pipeline | **EXISTING — source/CI verified** | [API main](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/api/main.py) registers task analysis/run and tool catalog routes and wires the existing task service/runtime. Main CI and Integration/Security pass. |
| Runtime guardrails, tool policy, approvals and audit/run storage | **EXISTING — source/CI verified** | Runtime, approval/audit, and [SQLite run store](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/core/state_store.py) exist with dedicated unit/integration/security tests. Deployment durability/tenant isolation still need separate validation. |
| API identity/authentication | **EXISTING, but not SaaS workspace auth** | [`backend/api/auth.py`](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/api/auth.py) compares a configured shared bearer API key. No per-user session/workspace identity is wired through these API dependencies. This is a foundational blocker before cross-user product data is implemented. |
| User settings persistence | **GAP / BLOCKED for multi-user SaaS** | [`backend/api/settings.py`](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/api/settings.py) fixes the actor to `DEFAULT_USER`; [`backend/core/settings.py`](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/core/settings.py) stores settings in a Python dictionary. Changes are not durable across process restart and are not separated by authenticated users. |
| Existing backend-served workspace UI | **EXISTING** | The current FastAPI app serves `backend/web/index.html`, `ui.js` and `ui.css`. This is distinct from the newer Next.js prototype. Detailed browser acceptance was not performed here. |
| Next.js command-center dashboard / AI workspace / workflow canvas | **PROTOTYPE — PR #173 only** | PR remains draft. Metrics/activity are illustrative; workflow nodes are client-side draft state, with no real persistence/execution connection; production build fails on CSS. |
| Durable student projects, tasks, kanban/backlog | **PLANNED / not verified on main** | No complete authenticated workspace/project/task domain API or storage slice was identified in the audited API registration and main tree. Do not show mocked tasks as live data. |
| AI model providers | **EXISTING, configuration-dependent** | [API setup](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/api/main.py) conditionally wires OpenAI or local Ollama gateway when environment flags are configured. This audit did not test real credentials or make live provider requests. |
| Run history / approvals | **EXISTING primitives** | API routers and SQLite state/approval components exist; SaaS ownership/tenant filtering still needs an explicit approved contract and tests before sharing data across users. |
| Scheduling primitives | **PARTIAL** | Schedule stores, pipeline and worker modules exist. A full student assignment connector/sync path was not verified. |
| WhatsApp inbound | **BLOCKED for end-to-end integration** | [`backend/channels/whatsapp_inbound.py`](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/channels/whatsapp_inbound.py) checks the webhook signature, then raises `NotImplementedError` for provider payload mapping. Signature/webhook primitives are not a working inbound-to-queued-task flow. |
| Campus/LMS assignment connector | **PLANNED / provider decision required** | No campus/LMS-specific module was found in the audited main source tree. No provider-specific authorized API, consent model or sync checkpoint is verified. Do not build a generic unauthorized scraper. |
| Node-based workflow persistence/execution | **PLANNED; UI draft only in PR #173** | No durable workflow-definition/version/run API group was observed in the main FastAPI route registration. Existing scheduler primitives are not proof of a visual workflow engine. |
| ERD/diagram tooling | **PARTIAL primitive** | [Diagram artifact validator](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/core/diagram_artifact_validator.py) exists. The complete versioned visual editor, renderer, and export workflow is not verified. |
| GitHub Developer Studio / subscription / usage billing | **PLANNED / not verified on main** | These appear in the product blueprint as targets; this audit found no end-to-end implementation/API slice to mark delivered. |
| Production deployment | **NOT VERIFIED / NOT CLAIMED** | Container Release passes, and a protected deployment workflow exists. No real production rollout/health/rollback evidence is attached to the audited main commit. |

## 5. Highest-priority gaps and risks

1. **HIGH — account/workspace/tenant contract:** the current shared API key plus fixed settings identity is not sufficient for an authenticated multi-user student workspace. Resolve C-001/C-002/C-004 and ownership policy before building shared tasks, artifacts, approvals or integrations.
2. **HIGH — frontend build is blocked:** fix the malformed CSS, add the lockfile strategy, rerun install/lint/build on the current PR head, then perform real desktop/mobile browser review. Keep PR #173 draft until evidence is clean.
3. **HIGH — WhatsApp inbound mapping is unfinished:** do not claim connected inbound commands until provider mapping, account binding/consent, signature, idempotency, queueing and saved-artifact tests work end-to-end.
4. **HIGH — unverified campus-provider permissions:** select one authorized pilot and official access path before connector implementation.
5. **MEDIUM/HIGH — duplicate/stale arithmetic PR candidate:** inspect the diff between #165 and merged #168; do not merge old-base code simply because an earlier CI run passed.
6. **HIGH — production rollout:** release build success is not deployment. Production stays incomplete until a real approved target is configured and deployed/checked, with rollback evidence.
7. **MEDIUM — frontend reproducibility and UX proof:** no frontend lockfile appears in PR #173 and no browser screenshot/smoke evidence was gathered in this audit.
8. **PROCESS BLOCKER — GitHub Project:** the available GitHub connection in this session does not expose a Project write operation; Project existence/visibility is inconclusive. Issue #182 must stay blocked until an authorized Projects-capable path verifies/reuses or creates a board and checks item linkage.

## 6. Recommended next actions

1. **#178 / A4 with independent A12 review:** fix the build blocker in a scoped PR, establish lockfile/install policy, rerun frontend CI on the latest base/head, and attach real desktop/mobile/browser evidence. Do not merge PR #173 by appearance alone.
2. **#179 / A1:** define student journeys, persona/role permissions, privacy/academic-integrity boundaries and provider decisions. Keep provider-specific unknowns explicit.
3. **#181 / A0 with A5 and A12:** draft actor/session/workspace, authorization/tenant, settings persistence, task/run state, API error, artifact ownership and webhook-idempotency contracts. Do not label them FROZEN before domain/security/owner review.
4. **PR #165:** compare against merged #168 file-by-file and recommend close as superseded only if the remaining unique diff has been checked; no merge while non-mergeable.
5. **#182:** obtain/verify GitHub Projects access, inspect for an existing suitable board first, then link the canonical issues without duplicates.
6. Do not expand to campus connectors, billing, a generic workflow runtime or real production deployment until upstream contracts and owner decisions are recorded.

## 7. Audit limitations and sign-off

- This document is based on GitHub source and recorded workflow metadata for the commit above.
- Product-code tests were not run locally as part of this audit. Main CI and Integration/Security did pass on the audited SHA; UI/browser/production checks were not run here.
- This is not an independent A12 sign-off. A12 review is **PENDING** and must record findings against the actual diff/evidence before the baseline ticket is accepted.
- Re-audit if `main`, any relevant PR head, workflows, provider configuration or deployment environment changes.
