# Frontend Prototype — Control Inventory

**Applies to:** PR #188, head `392f83a53d835642081468dba9f650a2383e934b`  
**Reviewed source:** `frontend/app/page.tsx` and the passing Playwright smoke test in Frontend CI run [38921695815](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38921695815).  
**Purpose:** distinguish working local prototype interactions from actions that are not connected to real product services. This is not a production-readiness statement.

## Status definitions

- **FUNCTIONAL (local UI):** the action has an observable effect in the running browser, but it may not persist or call the backend.
- **PROTOTYPE:** the control is illustrative or only shows a message / changes a local route; its advertised product operation is not implemented. Do not describe it as a live integration.
- **DISABLED:** the user cannot activate the control. A visual lock/disabled appearance is not equivalent to a semantic disabled state; the current prototype has decorative lock/toggle indicators noted below.

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
| Zoom in / zoom out / fit canvas | PROTOTYPE | Shows notices only; canvas scale or layout is not changed. |
| Node library entries | PROTOTYPE / inert | Buttons currently have a non-mutating handler; clicking them does not add/configure a node. |
| Execution mode select | PROTOTYPE (local form state only) | A value can be selected in the browser, but it is not saved or applied to an execution engine. |
| “Require approval”, “Audit every step”, “Allow unrestricted shell” indicators | PROTOTYPE / informational | Rendered as visual spans, not real toggle controls. The restricted-shell marker is a policy illustration, not runtime enforcement. |
| “Drag-and-drop coming next” | PROTOTYPE / informational | Drag-and-drop is not implemented. |

## Placeholder modules

| Control | Status | Actual behavior / limitation |
|---|---|---|
| Agents, Runs, Approvals, Integrations, Settings navigation | FUNCTIONAL (local UI) | Opens each placeholder page shell. |
| “Back to overview” | FUNCTIONAL (local UI) | Navigates to Overview. |
| Placeholder module copy and status icons | PROTOTYPE / informational | Communicates roadmap intent; does not prove the module is implemented. |

## Known gaps and acceptance boundary

- No true authentication/session, multi-tenant workspace selection, task API, durable workflow storage, workflow runtime, AI-run API, real notification source, campus provider, WhatsApp integration or billing integration is connected by this frontend PR.
- Decorative switches and node-library entries are not semantic disabled controls. They are called out here as prototype items instead of implying that they work.
- The smoke test checks a narrow path: Overview renders and shows the illustrative-data disclosure; local navigation opens the workflow canvas; adding a draft node changes the local node count; the mobile navigation drawer opens. It is not a comprehensive accessibility audit or full user-journey test.
- Separate follow-up work is required before any control listed as PROTOTYPE is represented as live behavior. Add functional browser/contract tests for each newly connected API-backed operation.

## Latest verified evidence

- [CI run 38921695937](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38921695937): PASS.
- [Integration and Security run 38921695812](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38921695812): PASS.
- [Frontend CI run 38921695815](https://github.com/Fbi-Boy/universal-task-ai/actions/runs/38921695815): PASS, including `npm ci`, lint, production build, Playwright smoke test, and screenshot artifact upload.

These results are for the cited PR #188 head only; refresh checks if that head changes.
