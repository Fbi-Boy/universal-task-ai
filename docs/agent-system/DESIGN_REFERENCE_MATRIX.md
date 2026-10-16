# Universal Task AI — Design Reference Matrix

This matrix is paired with [Agent Operating System](AGENT_OPERATING_SYSTEM.md) and the [Visual Reference Board](DESIGN_REFERENCE_BOARD.html). These are research starting points, not automatic design approval. The Sprint 0 app-shell/overview and AI-workspace clusters have reference cards and are **READY FOR OWNER REVIEW**, not approved. See [product requirements draft PR #184](https://github.com/Fbi-Boy/universal-task-ai/pull/184). No production UI implementation is authorized until the owner approves the selected direction.

| Screen area | Primary visual reference | Behavior/implementation reference | Direction to carry into UTA |
|---|---|---|---|
| Overview/app shell | [Planora dashboard](https://dribbble.com/shots/27758844-Planora-Project-Management-Dashboard), [AI task manager](https://dribbble.com/shots/25451888-AI-Task-Manager-SaaS-web-app), [Triangle responsive task dashboard](https://www.behance.net/gallery/120428393/SAAS-Task-Management-Dashboard-UXUI-Design), [Katonic Workroom](https://www.katonic.ai/workroom) — [section board](DESIGN_REFERENCE_BOARD.html#overview-shell) | [shadcn components](https://ui.shadcn.com/docs/components), [Next.js dashboard starter](https://github.com/Kiranism/next-shadcn-dashboard-starter) | Persistent sidebar/topbar, responsive task context, one restrained accent, understated surfaces, genuine metrics only; **READY FOR OWNER REVIEW** |
| AI workspace/chat | [AI chat dashboard](https://dribbble.com/shots/26609268-Case-Study-AI-Chat-Dashboard-Dark-Mode-UI), [ChatFusion workspace](https://dribbble.com/shots/26980076-ChatFusion-AI-Workspace-Dashboard-UI), [Katonic Workroom](https://www.katonic.ai/workroom), [Katonic ACE chat](https://www.katonic.ai/), [TextFusionAI chat + document](https://www.textfusionai.com/) — [section board](DESIGN_REFERENCE_BOARD.html#ai-workspace) | Existing UTA run/approval APIs and [shadcn components](https://ui.shadcn.com/docs/components) | Composer + conversation history + project context + truthful run/tool/status timeline + saved artifact context; permissions/errors visible; do not assume screenshots prove API behavior; **READY FOR OWNER REVIEW** |
| Tasks/kanban | [Kanban Board](https://dribbble.com/shots/11528230-Kanban-Board-White), [Flowboard](https://dribbble.com/shots/27058122-Flowboard-Project-Management-Dashboard-UI) | [ClickUp views](https://help.clickup.com/hc/en-us/articles/6310383076503-Task-views), [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) | List/board/calendar are views over one task entity; consistent status, filters and pagination |
| Campus Hub/assignment | AI task manager composition reference | [Moodle Web Services](https://docs.moodle.org/dev/Web_services) for one possible LMS; actual selected campus docs are authoritative | Course + source + deadline + sync state + consent + reminders; explicitly name each supported LMS |
| Automation/workflow builder | [SaaS workflow canvas](https://dribbble.com/shots/27362769-UI-UX-for-SaaS) | [n8n docs](https://docs.n8n.io/), [xyflow/React Flow](https://github.com/xyflow/xyflow) | Node palette/canvas/inspector, typed I/O, graph validation, versions, separate executions view and safe runtime |
| Workflow run detail | [n8n workflow discussions](https://community.n8n.io/t/how-to-create-a-staging-copy-of-an-n8n-workflow-before-going-live/293744) | [n8n official docs](https://docs.n8n.io/) | Per-step timeline, logs, retry, pause, error, approval, workflow version; never fake execution state |
| Developer Studio/GitHub | [GitHub Projects](https://github.com/features/issues) | [GitHub Projects docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) | Issue/PR/repository relations, filters, assignees/status, least-privilege connection and explicit repository selection |
| ERD | [dbdiagram.io](https://dbdiagram.io/) | [Eraser Diagrams repo](https://github.com/eraserlabs/eraser-diagrams) | Entities, types, PK/FK, cardinality, schema navigation, source text, validation, versioning and export |
| DFD/flowchart/UML | [Eraser Diagrams](https://github.com/eraserlabs/eraser-diagrams) | [xyflow/React Flow](https://github.com/xyflow/xyflow) plus a specific grammar for every format | Separate schemas and validators; do not advertise unsupported diagram renderers |
| Integrations/catalog | [sem.chat SaaS dashboard](https://sem.chat/ru/documentation) | Official provider documentation | Connected/disconnected/expired/error, scopes, last sync, reconnect/revoke; never expose credentials |
| Usage/plan | SaaS usage dashboard pattern | [Next.js dashboard starter](https://github.com/Kiranism/next-shadcn-dashboard-starter) for layout only | Real usage/quota/reset/entitlement/payment state; transparent limit/retry/cancel paths |
| Workspace members/settings | [Next.js dashboard starter](https://github.com/Kiranism/next-shadcn-dashboard-starter) | [shadcn components](https://ui.shadcn.com/docs/components) | Role-aware forms, destructive confirmations, session revoke and tenant isolation |
| Internal platform admin | Dashboard starter only as layout inspiration | Internal support workflow, audit and least privilege | Separate role surface, scoped support actions, explicit reason and audit; no silent tenant content access |

## Sprint 0 reference review — 16 October 2026

The current [Visual Reference Board](DESIGN_REFERENCE_BOARD.html) retains the ten original cards and adds page-specific evidence for the first two clusters. Source pages/images were checked on 16 October 2026. Where source publication dates were not stated, cards say so rather than inventing them.

| Cluster | Screenshot references | Domain coverage | Research result | Decision |
|---|---|---|---|---|
| [App shell + Overview](DESIGN_REFERENCE_BOARD.html#overview-shell) | R01 Planora; R02 AI Task Manager; R11 Triangle responsive task dashboard; R12 Katonic Workroom | 4 references across Dribbble, Behance and Katonic official product page | Navigation, project/task hierarchy, responsive task context and history reviewed. See individual cards for adopt/reject and image/source notes. | **PROPOSED · READY FOR OWNER REVIEW** |
| [AI Workspace + artifact context](DESIGN_REFERENCE_BOARD.html#ai-workspace) | R03 AI Chat Dashboard; R04 sem.chat SaaS settings/usage reference; R13 ChatFusion; R14 TextFusionAI; R15 Katonic ACE chat | 5 visual cards across Dribbble, TextFusionAI and Katonic; R04 sem.chat direct page could not be fetched in this pass and remains visual-only pending manual verification | Composer/history, tool affordance, chat/document context and status clarity reviewed. R04 supports settings/integration states rather than being treated as an AI-chat reference; do not rely on its interaction semantics until manually verified. | **PROPOSED · READY FOR OWNER REVIEW** |

### Unified recommendation

- **Shell:** mostly light neutral canvas, persistent clear navigation, readable page title/primary action, one restrained brand accent, consistent semantic status colors and a compact information hierarchy.
- **Overview:** show deadlines, tasks, runs and integration health only when backed by current APIs; empty/demo accounts must not show invented live metrics.
- **AI workspace:** use a primary conversation/composer area with explicit run/tool/approval state and accessible source/artifact context; responsive mobile layout stacks context panels rather than squeezing desktop columns.
- **Shared system:** reuse current typography/spacing/icon/component decisions. A darker, denser canvas can be considered for workflow/diagram editing but must use the same semantic tokens.
- **Reject:** copying brands/assets, KPI filler, persistent arbitrary gradients, oversized hero content that pushes tasks down, unclear authorization controls, nonfunctional buttons and inconsistent per-page tokens.

### Owner approval status

`PROPOSED / READY FOR OWNER REVIEW` as of 2026-10-16; **not approved**. Product requirements are still draft in [PR #184](https://github.com/Fbi-Boy/universal-task-ai/pull/184). A0 reviews fit against journeys, A3 checks token/system consistency, and the product owner must explicitly approve or request changes before any production UI implementation. These screenshot references do not demonstrate backend integration, responsive correctness in UTA, accessibility compliance or license rights for reusing original assets.

## Mandatory expansion per ticket

For each new route/page cluster, A2 must add 3–5 screenshot references from at least two domains, screenshot and direct source URL, creator/product, date checked, pattern adopted, pattern rejected, rationale, responsive/mobile notes, accessibility notes and a single recommended direction. A0 records owner approval before production UI code starts. A page engineer must not swap in an unrelated reference without reopening the decision.

## Role-specific visual review

- **Student:** task inbox, assignment detail, AI chat, notifications and own usage.
- **Workspace Owner/Admin:** member/permission management, integration connections, workflow publishing and workspace billing.
- **Member/Collaborator:** assigned tasks, project board, approved runs and shared artifacts.
- **Viewer/Reviewer:** read-only project/artifact access and explicit review/approval states.
- **Platform Support/Admin:** isolated internal control plane with scoped support/audit; no implicit access to private content.

Reuse a shared shell when roles differ only by permissions; provide screenshots/callouts for the exact differing navigation/actions instead of inventing separate design systems.

## Initial design synthesis

Do: calm neutral technical workspace, high contrast, one brand accent, semantic status colors, compact readable data density, shared app shell, consistent icons, clear real system states, keyboard and responsive support.

Do not: copy a reference literally; mix unrelated gradients/styles; use decorative emoji/icons everywhere; invent KPI charts; make fake data look live; leave inert actions; give each page a new spacing/radius/token system. Workflow/diagram editors may use denser/darker work surfaces, but must share semantic tokens.

## Official/code pattern sources

- [shadcn/ui source](https://github.com/shadcn-ui/ui) — reusable primitives and composition.
- [shadcn/ui docs](https://ui.shadcn.com/docs/components) — component behavior and accessibility.
- [React Flow / xyflow](https://github.com/xyflow/xyflow) — node/edge canvas candidate; check current license/version.
- [Eraser Diagrams](https://github.com/eraserlabs/eraser-diagrams) — diagrams-as-code patterns.
- [ClickUp views](https://help.clickup.com/hc/en-us/articles/6310383076503-Task-views) and [GitHub Projects docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) — product-management behavior.
- [n8n docs](https://docs.n8n.io/) — workflow behavior; evaluate license before embedding or offering customer-configurable workflows.
- [Next.js docs](https://nextjs.org/docs) and [FastAPI docs](https://fastapi.tiangolo.com/) — implementation references.

The screenshot references are for internal research. Do not copy logos, artwork or proprietary assets into the product without rights. Reference screenshots do not prove behavior or integration.
