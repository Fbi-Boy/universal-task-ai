# Sprint 0 — Product Requirements & Student Workflow Brief

**Status:** DRAFT FOR OWNER REVIEW — not an approved product scope  
**Prepared:** 16 October 2026  
**Canonical issue:** [#179 — Document student workflows, personas, roles and provider decisions](https://github.com/Fbi-Boy/universal-task-ai/issues/179)  
**Baseline:** `main` at `0f4151c067815106d6600f47bab403e5e674c64c`  
**Purpose:** Give product/design/architecture agents one shared, evidence-linked brief. The document identifies decisions; it does not silently make product, provider, privacy, financial or production decisions for the owner.

## 1. Product definition

Universal Task AI is intended to become **one student productivity and IT developer workspace**. A student should be able to capture coursework tasks, plan projects, ask AI for bounded help, review generated work, save versioned artifacts and receive notifications through approved channels. Developer tools and automation should build on the same task, identity, permission, artifact and audit concepts.

The product must not be delivered as unrelated demo pages. A screen is not a completed feature unless it uses the approved data contract, permission model, real loading/empty/error/success states, and an end-to-end acceptance scenario. Example metrics or activity must never appear as live user data.

**Current state caveat:** the product vision and blueprint are target design, not proof of implementation. The audited backend has a real FastAPI task/runtime foundation and a backend-served workspace. PR #173 is a separate draft Next.js UI prototype; its metrics/activity are illustrative and live task/workflow persistence/execution are not connected. Current audit evidence and open gaps are recorded in [Issue #177](https://github.com/Fbi-Boy/universal-task-ai/issues/177) and [the baseline audit proposed in PR #183](https://github.com/Fbi-Boy/universal-task-ai/pull/183).

### Product outcomes

1. A student can collect deadlines in one place and see the source and last-sync state of imported assignments.
2. Manual and imported work use the same task/project model rather than separate, duplicate lists.
3. AI runs through the current bounded runtime; the user can see honest status, approvals, errors and outputs.
4. Results that should persist are saved as artifacts with ownership, version, provenance and permission checks.
5. WhatsApp and campus inputs enter the same authenticated, normalized and deduplicated task pipeline.
6. Workflow automation is a saved, versioned and server-validated definition—not merely a canvas drawing.
7. Developer tools expose GitHub context and versioned diagrams with explicit repository permissions.
8. Usage limits and provider failures are enforced server-side and explained clearly.
9. The experience is visually coherent, accessible, responsive and evidence-tested across key states.

## 2. Personas and permission boundaries

These are proposed product personas, not accounts/roles already implemented in the audited backend.

| Persona | Primary job | Allowed capabilities (target) | Must not receive implicitly |
|---|---|---|---|
| **Personal Student** | Organize own coursework and IT work | Create/manage own tasks/projects, connect approved personal integrations, request AI drafts, review/download own artifacts, manage own notification consent | Access to another person's records; silent official submissions; attendance spoofing |
| **Workspace Owner/Admin** | Configure a shared workspace | Manage members/roles, workspace settings, allowed integrations, shared projects and workflow publishing within granted scope | Hidden access to credentials; privilege elevation from AI output; platform-wide access |
| **Member/Collaborator** | Complete assigned/shared work | Work on projects/tasks shared with the member; run permitted AI workflows; access authorized artifacts | Access to unshared tasks, private conversations, other workspaces or connection secrets |
| **Viewer/Reviewer** | Inspect work and provide review/approval where granted | Read permitted project/artifact details, comment or approve an explicitly scoped action | Execute/write permissions merely because a review link is visible |
| **Platform Support/Admin** | Operate the service safely | Minimal operational metadata and audited support actions under a separate control-plane policy | Implicit access to private student content or the ability to act as a student |

### Authorization rules

- The server derives actor and workspace context from authenticated identity, never from an untrusted `user_id` or `workspace_id` supplied in a request body.
- Every task, project, conversation, run, approval, event, artifact, integration and workflow must have explicit ownership and a server-side permission check.
- Background workers and webhook handlers enforce the same scope checks as interactive API routes.
- Cross-workspace reads/writes must fail closed. Shared records require an explicit sharing grant.
- Role names are not a substitute for resource/action-level authorization. Each protected action must specify who can do it and which resource it can affect.
- The current global API-key authentication and fixed `DEFAULT_USER` settings model are not accepted as the target multi-user SaaS contract; see [shared contract register](../07_SHARED_CONTRACT_REGISTER.md), C-001/C-002/C-004.

## 3. End-to-end student journeys

Each journey is an acceptance target. It does not imply the connected provider/API already exists.

### J1 — Authorized campus source → assignment → task → notification

**Actor and trigger:** a student chooses a supported campus source and explicitly connects/authorizes it; or an allowed provider event arrives for an existing connection.

**Happy path**
1. Explain the provider, requested scopes/data, last-sync semantics and disconnect/revoke behavior before connection.
2. Validate provider authorization and store only protected credential references, never expose credentials in the UI.
3. Read changes from the official/authorized source using bounded requests and a saved checkpoint.
4. Normalize each event into a consistent assignment record: provider, external ID, course, title, description, deadline/timezone, official source URL, changed/deleted state and last-seen metadata.
5. Deduplicate with a stable key scoped to the workspace/provider/external assignment ID. Updates to the same assignment modify the existing task/link; they do not create a second task.
6. Show the assignment with a source link and sync status, then apply the user's notification preferences to send a concise alert.
7. Allow the student to convert/update the assignment in My Tasks and ask AI for a draft plan; retain provenance back to the official source.

**Failure/recovery:** revoked/expired access, unsupported provider, timeout/rate limit, invalid payload, missing deadline, changed/deleted assignment, duplicate webhook/poll, denied scope and user-disconnect. Preserve the last known data with a stale/failed sync indicator; retry only safe/idempotent operations with bounded backoff. Never claim a current sync if the provider did not answer.

**Required decisions:** first campus/LMS provider; approved API/consent; data fields and retention; sync frequency/rate limits; notification channel and quiet hours. No campus provider is selected by this brief.

### J2 — Manual task / project / backlog → focused work

**Actor and trigger:** a student creates a task manually, turns an authorized assignment into a task, or creates a task inside a project.

**Happy path**
1. Choose a project or Personal Inbox.
2. Enter title, description, deadline/timezone, priority, labels, checklist/subtasks and references; keep required fields minimal for quick capture.
3. Show a real saved/pending/error state. When persistence is available, return the server-created canonical ID.
4. Show the same task in list, kanban and calendar views, with filtering and sort semantics applied to real data.
5. Support explicit status transitions, dependency validation and a reversible edit path; do not display controls that have no implementation.
6. Open task detail to see source, owner/workspace, comments, attachments/artifacts, activity and available actions.

**Failure/recovery:** offline/timeout, duplicate submit, invalid deadline/timezone, deleted project, permission denial, conflicting update and stale view. Display unsaved changes clearly; use idempotency or conflict handling as contracts specify; never show optimistic success that is not reconciled with server state.

**Acceptance scenarios**
- Given a task is saved, when the page reloads, the task remains present for the same authorized actor.
- Given a user is not a member of another workspace, when they request its task by ID, the API denies access.
- Given an assignment has already been imported, when the same source event is replayed, no duplicate task is created.
- Given a task cannot be saved, when the request fails, the UI shows an error and preserves recoverable user input.

### J3 — AI request → bounded run → reviewed artifact

**Actor and trigger:** a student asks the AI Workspace to explain, plan, research, draft or execute a bounded permitted task.

**Happy path**
1. Capture the request and its context from authorized tasks/files only. Clarify missing goal, output format, boundaries or deadline when required.
2. Analyze the request and produce a plan/routing summary. The plan never grants the model new tool permissions.
3. Execute through the existing server-side runtime/tool boundary. Use explicit authorization and human approval for sensitive side effects. Long-running work needs a durable run/job state and a cancellation/retry model.
4. Report truthful state transitions, tool activity, safe error summary and request/correlation ID where available.
5. Validate the result; save an artifact with owner/workspace, MIME type/size, version, timestamp, source/provenance and download/access policy where applicable.
6. Present the result for review. The student can read, revise, copy/download supported outputs or request changes; external academic submission requires a supported platform path and explicit user confirmation.

**Failure/recovery:** model provider unavailable/quota exceeded, unsafe/unavailable tool, no tool matches, needs input, approval timeout/rejection, execution timeout/cancel, output validation failure, artifact storage failure and duplicate retry. Failed or unsupported work cannot show success. Avoid repeating side effects when retrying a job.

**Acceptance scenarios**
- Given a request cannot be performed by an available tool, when the run ends, its status clearly says it needs a tool or failed instead of claiming success.
- Given a sensitive action requires approval, no side effect runs until the correct actor's approval is durably recorded and consumed once.
- Given a draft artifact is saved, an authorized user can retrieve it after process restart; an unauthorized workspace cannot.
- Given the model provider is unavailable, the UI reports the provider failure without fabricating output or exposing credentials.

**Status decision required:** the current runtime uses states including `succeeded` and `needs_tool`; the target blueprint examples also use `completed`, `needs_input` and `ready_for_review`. A0 must resolve the canonical task/run lifecycle and mapping in C-005/C-006 before frontend or worker code invents a new vocabulary.

### J4 — WhatsApp opt-in / command / result notification

**Actor and trigger:** a student explicitly enables WhatsApp notifications and links a provider identity to the correct authenticated account. A message arrives through the approved provider webhook or the system sends a permitted notification.

**Happy path**
1. Explain opt-in, message categories, privacy implications, delivery failures, quiet hours and how to disconnect.
2. Validate webhook signature, bound payload size, parse the provider's real envelope, normalize sender/message ID/text/time and resolve the previously linked account.
3. Reject unknown/unlinked senders, invalid signatures and unsupported commands. Deduplicate provider message IDs and verify the sender's current permissions before creating a task/run.
4. Enqueue a bounded command; do not block the webhook request on long AI execution.
5. Send safe acknowledgements and permitted status notifications. Artifact links must require proper authentication/authorization or short-lived, scoped access.
6. Record delivery state and provide in-app fallback when the provider fails or the user opts out.

**Failure/recovery:** bad signature, replay, duplicate event, unlinked sender, rate limit, malformed/oversized payload, ambiguous command, provider outage, opt-out and outbound delivery failure. Do not leak private task content to an unverified phone number. Do not execute a high-impact side effect from an ambiguous message without explicit confirmation.

**Current-state note:** the existing inbound adapter verifies a signature but throws `NotImplementedError` for provider payload mapping. Full inbound command execution is therefore a blocked target, not a shipped integration.

**Required decisions:** official provider/API, account-linking verification method, opt-in UX, supported command set, outbound templates and user-visible budget/limits.

### J5 — Workflow draft → validated version → observable execution

**Actor and trigger:** a workspace-authorized user creates or edits a workflow, publishes a version and triggers it manually or through an allowed event/schedule.

**Happy path**
1. Choose from a small, approved node catalog; configure trigger, inputs, variables, conditions and outputs using typed schemas.
2. Validate graph structure server-side (node types, required inputs, graph size/depth, secret references, permissions, cycles and unavailable nodes).
3. Save a versioned immutable definition; editing a draft must not silently mutate a running version.
4. On trigger, verify actor/workspace, opt-in, permission, schedule/event constraints and idempotency key before queuing a run.
5. Execute nodes using a trusted worker and existing bounded tool/runtime contracts; show step-level status, start/end time, safe log, output reference, retry and approval boundary.
6. Support safe pause/cancel/retry according to explicit lifecycle semantics; preserve the exact workflow version and step trace for review.

**Failure/recovery:** invalid/cyclic graph, removed integration, expired credential, duplicated trigger, timeout, partial failure, retry after external side effect, user cancellation and workflow version changed during a run. A canvas can edit a draft; it is never an execution or permission authority.

**Current-state note:** PR #173 is a client-side visual draft. The audited main API did not expose a durable workflow definition/version/run domain. Scheduler primitives are useful building blocks but are not a complete n8n-like runtime.

**Required decisions:** initial safe node set, licensing/embedding review if reusing third-party workflow components, trigger types and resource/budget ceilings.

### J6 — Developer Studio: GitHub context and versioned diagrams

**Actor and trigger:** an IT student explicitly connects GitHub and chooses an authorized repository, or opens a diagram document in a project.

**Happy path**
1. Explain requested GitHub scopes and choose a repository explicitly; provide disconnect/revoke.
2. Start with read-only repository/branch/commit/issue/PR context. Any operation that writes or opens a PR requires a separate permitted scope and explicit user confirmation.
3. Create a diagram from typed source, validate the supported format, render it, and persist versioned source plus render metadata.
4. Support history/compare and exports only for formats that have real parsers/renderers/tests. Every artifact belongs to an authorized project/workspace.
5. Show permission denied, revoked connection, unsupported format and validation errors clearly.

**Failure/recovery:** expired/revoked token, repository access denied, provider rate limit, malformed/unsafe source, unsupported syntax, renderer failure and export size limits. Never include secrets in prompts, output, logs or images.

**Current-state note:** a diagram artifact validator exists, but this does not establish a full visual editor/version/render/export experience. End-to-end GitHub connection and diagram-document APIs remain target scope.

**Required decisions:** first read-only GitHub slice, required scopes, write-action confirmation rules, supported diagram formats and licensing of editor/rendering libraries.

### J7 — Attendance and schedule reminders

**Actor and trigger:** a student manually adds a schedule or imports an authorized schedule, then chooses reminder timing and timezone.

**Happy path:** normalize the event time, show the official attendance/class link, schedule a reminder, notify with enough lead time, and let the student open the official source and act for themselves. Show whether a reminder is scheduled, delivered, snoozed or cancelled.

**Non-negotiable boundary:** no spoofed attendance, simulated student presence, hidden check-in, identity deception, location falsification, or silent submission to an official academic system. A reminder and official-link navigation do not imply attendance is recorded.

**Failure/recovery:** timezone/DST change, cancelled class, duplicate schedule sync, notification permission disabled, provider outage and reminder not delivered. Show last-update/source and allow manual correction.

### J8 — Usage and plan visibility (later phase)

**Actor and trigger:** a student/owner views current limits, or a run requests a metered resource.

**Target behavior:** server-side usage ledger records attributable events idempotently; quota checks happen before expensive work; user sees current usage, reset semantics and actionable limit/retry options. Billing state comes only from a verified billing provider, never a client toggle. Do not start a paid-plan implementation before C-015 and the product owner decide pricing, budgets, retention and payment provider.

## 4. Cross-cutting requirements

### Identity, tenancy and data

- Each user-initiated request and background job must carry server-derived actor/workspace scope and re-authorize resource access.
- Use stable IDs, uniqueness constraints, pagination bounds and validated filter/sort fields.
- Contract specs must define data ownership, deletion/export, retention, cascade behavior, recovery and migration compatibility.
- Persist settings by authenticated user/workspace. Do not use `DEFAULT_USER` as a production multi-user identity.
- Do not put secrets, API keys, provider tokens, session cookies, real student data or personally identifying assignment content in screenshots, logs or committed fixtures.
- Define which source payloads are retained, what can be deleted, and how disconnect/revoke affects stored synced data.

### Statuses, errors and reliability

- A0/domain owners freeze canonical task, run, workflow, delivery and sync states before consumers are implemented.
- Define transitions and terminal states explicitly; no UI invents success status from HTTP 200 or an illustrative percentage.
- Use a consistent safe error envelope with request ID, validation details safe to show, retryability, and permission-denied semantics without internal secrets/stack traces.
- Bound input/output sizes, runtime, provider timeouts, concurrency, retries and cost. Avoid retries that duplicate external side effects.
- Use idempotency/deduplication for repeated submit requests, schedule events, webhooks, runs and usage events.
- Loading, empty, stale, unauthorized, disabled, partial failure, offline and recovery states are first-class requirements.

### Academic integrity and AI trust

- AI output is a draft for student review; show source/provenance and let the student inspect, revise and decide how to use it.
- Do not bypass course/platform rules or present generated work as an official submission performed without the student.
- No attendance spoofing or silent official actions.
- Untrusted assignment text, emails, web pages and provider payloads cannot grant tool permissions or override system security rules.
- Approval must be explicit, actor-bound, resource-bound, short enough-lived for the risk, auditable and consumed at most once.

### Integration, consent and user control

- Each integration has states such as not connected, connecting, connected, degraded, expired, revoked and error. The state must come from the actual provider/service and not from static demo values.
- Consent and notification preferences are stored, visible and revocable. Disconnect stops future sync/delivery and documents how retained data is handled.
- Use official/authorized provider APIs and permissions. No arbitrary credential scraping or generic campus login automation.
- Webhook signature checks alone are insufficient: mapping, account linking, payload limits, replay/deduplication and processing outcomes also need tests.
- Credentials stay server-side in a secret provider/credential vault; the UI receives only safe connection metadata.

## 5. Product-area and route catalogue

Current UI, target page, and permission-aware states must be distinguished. This catalogue guides reference research; it does **not** authorize production UI implementation before an approved board.

| Area / route cluster | Main persona | Minimum useful contents | Reference/approval gate | Delivery stage |
|---|---|---|---|---|
| Existing workspace at `/` | Personal Student / local developer | Current task composer, actual API/run/approval states | Audit current implementation; preserve its working contracts | Existing; current-state usability/contract checks required |
| Overview / command center | Student, workspace owner | Real upcoming deadlines, task counts only when sourced, latest runs, sync/connection health | **Needs page-specific board and owner approval**; reuse shell direction only after decision | After identity and API contracts |
| AI Workspace + task/run detail | Student, member, reviewer | Prompt, plan, run timeline, approval, result, artifact/provenance, errors | **Needs board and owner approval** | First integrated vertical slice |
| My Tasks / task detail | Student, member, reviewer | Inbox/today/upcoming, due/priority/status, list/kanban/calendar, source and task detail | **Needs board and owner approval** | After identity/persistence |
| Projects & backlog | Owner/admin, member, reviewer | Projects, members, backlog/board/list, milestones, task links | **Needs board and owner approval** | After task CRUD |
| Campus Hub / assignment detail | Student | Connected provider status, courses/assignments, source link, deadline and sync health | **Needs board and owner approval**; connector decision first | After provider selection |
| Schedule / attendance reminder | Student | Event time/timezone, reminder controls and official source link | **Needs board and owner approval**; reminder-only safety boundary | After schedule data source |
| Integrations / connection detail | Owner or authorized student | Provider status, permission/scopes, last sync, revoke/reconnect, error/consent | **Needs board and owner approval** | Alongside approved connector |
| WhatsApp preferences/links | Student, owner where shared | Opt-in, linked account status, notification categories, disconnect | **Needs board and owner approval**; don't fake "connected" | After provider selection |
| Workflow builder + run inspector | Owner/member/reviewer | Typed nodes/edges, draft/version, validation, run steps, logs, approvals and retry | **Needs board and owner approval**; workflow API/contract first | After typed workflow schema |
| Developer Studio / GitHub repository | IT student, member | Explicit repo picker, safe branch/commit/issue/PR context and permissions | **Needs board and owner approval** | After auth + GitHub scopes |
| Diagram editor / history/export | IT student, member | Supported format/source, validation, render, version history/export | **Needs board and owner approval** | Separate format slices |
| Artifacts & Files | Student, member, reviewer | List/search, version/provenance, preview/download and permission errors | **Needs board and owner approval** | After artifact persistence contract |
| Workspace members/security | Owner/admin, platform support in separate control plane | Membership/roles, session/security state, audit, deletion confirmation | **Needs board and owner approval**; sensitive permissions review | After identity/workspace design |
| Usage & plan | Student, workspace owner | Actual usage ledger, limits, reset and verified billing status | **Needs board and owner approval** | Later, after C-015/product pricing decision |

### Existing backend API surface observed on the audited main

- `POST /v1/tasks/analyze`
- `POST /v1/tasks`
- `GET /v1/tools`
- `/health` and `/ready`
- Router groups for run history/events, approvals and settings are registered in `backend/api/main.py`; exact request/response, auth and persistence semantics must be read from the implementation before a client depends on them.

The route names below are **targets/examples only**, not a claim that these APIs exist: `/v1/auth/*`, `/v1/workspaces/*`, `/v1/projects/*`, project-backed `/v1/tasks/*`, `/v1/campus/*`, `/v1/integrations/*`, `/v1/automations/*`, `/v1/developer/*`, `/v1/artifacts/*`, `/v1/usage/*`, and `/v1/billing/*`. Confirm code/OpenAPI and freeze each relevant contract before implementation.

## 6. Product and provider decisions — must not be guessed

| Decision | Options to research (not a selection) | Decision owner | Evidence/inputs needed | Blocks |
|---|---|---|---|---|
| First campus source | Official LMS API/OAuth; another authorized campus API; allowed email notification ingestion; user-run read-only companion only if it complies with campus rules | Product owner, informed by A1/A8 | Campus name/domain, provider/API docs, available test tenant/account, permissions, rate limits and consent requirements | Assignment sync, Campus Hub |
| WhatsApp channel | Official provider API or a supported business messaging provider | Product owner + A8 | Provider account eligibility, API/webhook docs, template/opt-in rules, monthly pricing, test number and verification flow | Inbound commands/outbound notifications |
| Initial product identity | Local single-user developer mode plus separately designed multi-user SaaS auth; decide launch scope explicitly | Product owner + A0/A5 | Intended first users, invite/member model, login/session requirements, deployment and recovery constraints | Workspace data model and protected API endpoints |
| Product persistence | Preserve SQLite for local/test where appropriate; target durable shared database/object storage for hosted multi-user needs | Product owner + A0/A5 | Hosting constraints, backup/recovery, storage/retention requirements, migration operations and budget | Durable workspace, tasks and artifacts |
| AI provider/model and budget | Configured OpenAI gateway or supported local Ollama path; additional providers only after adapter/ops review | Product owner + A7 | Allowed provider, secret ownership, data handling terms, expected token/task volume, budget ceiling, timeout and fallback expectations | AI runs, artifact quality, usage tracking |
| Notification channels | In-app first; WhatsApp only after opt-in/provider decision; email/calendar only if selected later | Product owner + A8 | Preferred channels, quiet hours, privacy defaults, delivery/fallback expectations | Notification UX and delivery rules |
| Data retention/privacy | Retain minimum needed; define assignment payload, prompt, run logs, artifacts, connection metadata and deletion periods | Product owner + A0/A5 | Sensitive data inventory, user control requirements, retention/deletion/export needs and hosting policy | Workspace schemas, logs, artifacts, connectors |
| GitHub integration | Read-only repository selection first; write permissions separated by action and confirmed by user | Product owner + A10 | Repo ownership, required scopes, supported auth/install path, rate limits and approval expectations | Developer Studio, GitHub writes |
| First diagram formats | Implement only formats with a tested parser/renderer/export contract | Product owner + A10 | Target users' first formats, available libraries/licenses, sample fixtures and expected export | Diagram editor scope |
| Usage/billing | Usage visibility and enforcement before payments; payment provider deferred | Product owner + A0/A5/A7/A11 | Pricing/plan model, limits, provider eligibility, invoicing/refunds, webhook signing/reconciliation and budget | Billing implementation; not an early blocker for core free slice |
| First integrated vertical slice | Recommended candidate: authenticated user/workspace → one persisted task → AI run through existing safe runtime → reviewed artifact, visible from UI | Product owner approves; A0 recommends | Confirm scope, auth/session target, data contract, approved visual board and measurable acceptance scenario | Sprint 1 implementation start |

Record the decision, alternatives, rationale, affected tickets and review date in a durable ADR/decision log. Until a decision is made, implementation tickets must either be explicitly discovery-only or remain BLOCKED.

## 7. Recommended delivery order and quality gates

1. **Finish Sprint 0 evidence:** accept baseline audit after A12 review; reproduce/fix PR #173 build issue; complete product requirements; obtain page-specific owner design approval; draft/freeze only the contracts needed for the first slice.
2. **Identity and persistence foundation:** define actor/session/workspace/membership and resource ownership. Run cross-tenant negative tests for settings/runs/approvals/events/artifacts before adding multi-user resources.
3. **One thin task vertical slice:** real UI input → validated API → durable task/run → actual execution or honest needs-tool/error state → saved artifact → reload/retrieval with the correct owner.
4. **Student task and project model:** once identity and artifact/run contracts are verified, add CRUD and board/list states using real data.
5. **Integrations by authorization readiness:** complete WhatsApp payload mapping + linking/idempotency, then one campus connector with known provider permissions. Avoid starting both integrations as a broad batch.
6. **Workflow runtime after typed contracts:** versioned definitions and server-side graph/permission validation before connecting a visual canvas to execution.
7. **Developer Studio and usage/billing later:** use bounded independent slices after their ownership, credential and schema contracts are frozen.
8. **Release gate:** current-head CI, review, UI screenshots/accessibility, migration/rollback, recovery, health and owner approval; container build/rehearsal alone is not a production rollout.

For every user-visible slice, include: happy path; at least five relevant failure/security cases; role/tenant authorization tests; unit/API/integration/browser checks as applicable; mobile/keyboard/a11y review; exact command and current SHA; safe error/state evidence; source/reference and owner approval; docs/Program State updates.

## 8. Owner review checklist

- [ ] Confirm which university/campus/provider is the first connector target, or choose a non-campus first slice until that information exists.
- [ ] Decide whether the first milestone is local single-user mode, multi-user SaaS or both with separate auth paths.
- [ ] Approve the initial product journeys and the academic-integrity/consent boundaries.
- [ ] Choose or authorize research for WhatsApp provider, model provider/budget and persistence/deployment constraints.
- [ ] Confirm the first integrated vertical slice and what counts as success.
- [ ] Review and approve the shell/Overview and AI Workspace/task-detail visual reference boards before production UI changes.
- [ ] Review the relevant C-001–C-018 contracts; implementation remains blocked when an affected contract is ambiguous.
- [ ] Decide which future areas remain hidden/Coming Soon until their backend slice and QA are accepted.

**Approval state:** NOT YET APPROVED. Completing this document does not mean the owner has selected a provider, approved a design or authorized implementation.

## 9. Traceability

- [Program Charter](../00_PROGRAM_CHARTER.md)
- [Dependency Map](../03_DEPENDENCY_MAP.md)
- [Shared Contract Register](../07_SHARED_CONTRACT_REGISTER.md)
- [Design Research & Approval process](../06_DESIGN_RESEARCH_AND_APPROVAL.md)
- [Ticket Packet Template](../05_TICKET_PACKET_TEMPLATE.md)
- [Product & Engineering Blueprint — workflows and architecture](../../agent-system/chapters/blueprint-01-product-and-architecture.md)
- [Product & Engineering Blueprint — API/sprint roadmap](../../agent-system/chapters/blueprint-02-api-and-sprint-roadmap.md)
- [Canonical A0–A13 role definitions](../../agent-system/chapters/01-decisions-and-agent-roles.md)
- [Current API registration](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/api/main.py)
- [Current authentication](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/api/auth.py)
- [Current settings route](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/api/settings.py)
- [WhatsApp inbound adapter](https://github.com/Fbi-Boy/universal-task-ai/blob/main/backend/channels/whatsapp_inbound.py)
- [Open frontend draft PR #173](https://github.com/Fbi-Boy/universal-task-ai/pull/173)
