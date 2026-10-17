# Frontend Prototype — Control Inventory

**Applies to:** PR #188 frontend prototype. Node-library interaction is implemented in [`1de7f24`](https://github.com/Fbi-Boy/universal-task-ai/commit/1de7f24e0a84bf8bd50f351bd8b62956811db1b6); its smoke-test selector fix is in [`97d3014`](https://github.com/Fbi-Boy/universal-task-ai/commit/97d3014b8e3903a91a7a85f0905f38a6311ac794).  
**Reviewed source:** `frontend/app/page.tsx` and the passing Playwright smoke test in Frontend CI run [38927084454](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38927084454).  
**Purpose:** distinguish working local prototype interactions from actions that are not connected to real product services. This is not a production-readiness statement.

## Status definitions

- **FUNCTIONAL (local UI):** the action has an observable effect in the running browser, but it may not persist or call the backend.
- **PROTOTYPE:** the control is illustrative or only shows a message / changes a local route; its advertised product operation is not implemented. Do not describe it as a live integration.
- **DISABLED:** the user cannot activate the control. A visual lock is not equivalent to a semantic disabled state; the unrestricted-shell indicator remains a locked, informational marker.

## Overview and app shell

| Control | Status | Actual behavior / limitation |
|---|---|---|
| Main sidebar page items | FUNCTIONAL (local UI) | Switches the active local page shell; most modules are placeholders, not connected data views. |
| Mobile navigation open/close and backdrop | FUNCTIONAL (local UI) | Opens/closes the sidebar locally. Browser smoke covers mobile navigation. |
| “Explore workflows”, “Open editor”, “Explore automation” | FUNCTIONAL (local UI) | Navigates to the local workflow editor. |
| “New task”, “Open AI workspace” | FUNCTIONAL (local UI) | Navigates to AI Workspace only; it does not create or persist a task. |
| Workspace selector | PROTOTYPE | Shows a “Personal workspace selected” notice; it does not switch a real workspace. |
| Search control | PROTOTYPE | Shows a message that search will arrive with the workspace data API. No search is performed. |
| Notifications bell | PROTOTYPE | Opens the placeholder Approvals page. It does not read actual notifications. |
| Help | PROTOTYPE | Shows a message that the help center is a later integration. |
| User profile | PROTOTYPE | Opens the placeholder Settings page; it is not an authenticated profile or account menu. |
| “Last 7 days” date filter | PROTOTYPE | Shows a notice that live run analytics will populate metrics. It does not change chart data. |
| Dashboard metrics and activity rows | PROTOTYPE | All are illustrative preview data, now labelled in the UI. They are not account activity or live run analytics. |
| Activity “more” controls | PROTOTYPE | Show a notice that run details will be available with live run data. |
| Activity “View all” | FUNCTIONAL (local UI) | Navigates to the placeholder Runs page; actual run records are not loaded. |
| Featured workflow “Open editor” | FUNCTIONAL (local UI) | Opens the local workflow editor; no workflow record is fetched. |

## AI Workspace

| Control | Status | Actual behavior / limitation |
|---|---|---|
| Prompt textarea | FUNCTIONAL (local UI) | Accepts and edits local prompt text; does not submit until the user clicks the button. |
| Prompt suggestion chips | FUNCTIONAL (local UI) | Populate the textarea with the chosen sample prompt. |
| “Submit task” | PROTOTYPE | Empty input produces a validation notice. Non-empty input produces a notice that API integration is the next step; no task is created. |
| Sensitive-action approval message | PROTOTYPE / informational | Static explanation only; no approval request is created from this screen. |

## Workflow editor

| Control | Status | Actual behavior / limitation |
|---|---|---|
| Workflow name input | FUNCTIONAL (local UI) | Updates the name displayed in this in-memory draft only. It is not persisted. |
| “Add step” / “Add another step” | FUNCTIONAL (local UI) | Adds a node to the in-memory draft and shows a notice. Playwright smoke verifies the node count increases. |
| Workflow node selection | PROTOTYPE | Shows the selected node name in a notice; node properties are not editable/configurable. |
| “Test workflow” | PROTOTYPE | Shows a notice that execution is not connected. No workflow run is started. |
| Workflow “more” action | PROTOTYPE | Shows a notice that the workflow save API is not connected. No save occurs. |
| Zoom in / zoom out / reset zoom | FUNCTIONAL (local UI) | Changes the canvas display scale between 60% and 140%, in 10-point increments. Reset returns to 100%; the zoom is not persisted. |
| Node library search | FUNCTIONAL (local UI) | Filters node definitions by category, title and detail; it does not search persisted workflows or backend data. |
| Node library entries | FUNCTIONAL (local UI) | Clicking a library entry adds that node type to the in-memory draft and shows a notice; drag-and-drop, node configuration, persistence and execution remain unimplemented. |
| Execution mode select | PROTOTYPE (local form state only) | A value can be selected in the browser, but it is not saved or applied to an execution engine. |
| Require approval | FUNCTIONAL (local UI) | Accessible switch changes an in-memory draft boolean only; no runtime approval enforcement occurs. |
| Audit every step | FUNCTIONAL (local UI) | Accessible switch changes an in-memory draft boolean only; no audit events or logs are emitted. |
| Allow unrestricted shell | PROTOTYPE / informational | Remains visibly locked; no unrestricted shell is enabled. The marker is not a runtime policy control. |
| “Drag-and-drop coming next” | PROTOTYPE / informational | Drag-and-drop is not implemented. |

## Placeholder modules

| Control | Status | Actual behavior / limitation |
|---|---|---|
| Agents, Runs, Approvals, Integrations, Settings navigation | FUNCTIONAL (local UI) | Opens each placeholder page shell. |
| “Back to overview” | FUNCTIONAL (local UI) | Navigates to Overview. |
| Placeholder module copy and status icons | PROTOTYPE / informational | Communicates roadmap intent; does not prove the module is implemented. |

## Known gaps and acceptance boundary

- No true authentication/session, multi-tenant workspace selection, task API, durable workflow storage, workflow runtime, AI-run API, real notification source, campus provider, WhatsApp integration or billing integration is connected by this frontend PR.
- Approval and audit switches change local draft state only; runtime policy enforcement and audit logging are not connected. Unrestricted shell remains locked. Node-library entries add a selected node to the local draft, but this does not enable drag-and-drop, node configuration, persistence, or execution.
- The smoke test checks a narrow path: Overview renders and shows the illustrative-data disclosure; local navigation opens the workflow canvas; adding a Webhook from the node library and adding a generic draft step both change the local node count; the mobile navigation drawer opens. It is not a comprehensive accessibility audit or full user-journey test.
- Separate follow-up work is required before any control listed as PROTOTYPE is represented as live behavior. Add functional browser/contract tests for each newly connected API-backed operation.

## Latest verified evidence

- [CI run 38927084549](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38927084549): PASS.
- [Integration and Security run 38927084432](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38927084432): PASS.
- [Frontend CI run 38927084454](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38927084454): PASS, including `npm ci`, lint, production build, Playwright smoke test, and screenshot artifact upload.

These results are for the cited PR #188 head only; refresh checks if that head changes.
