# Universal Task AI — Premium Dashboard

A separate Next.js frontend workspace for the product dashboard and visual workflow builder.

## Run locally

```bash
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000.

## Validation

```bash
npm run lint
npm run build
npx playwright install chromium
npm run test:e2e
```

The Playwright smoke test launches the production build, checks that Overview renders, switches to the workflow editor, verifies that adding a draft step works, and captures desktop/mobile screenshots. It tests only prototype interactions, not backend persistence or real integrations.

## Current scope

- Responsive command-center dashboard shell with sidebar navigation.
- Overview page with product hierarchy, metrics preview, activity list, and workflow preview.
- AI Workspace UI.
- Visual workflow draft canvas with node library, connectors, editable workflow name, and add-step interaction.
- Workflow settings panel that makes approval and audit boundaries visible.
- Responsive mobile navigation and keyboard focus states.

## Important limitations

This is a **frontend prototype**, not a claim that every screen is connected to production services. Dashboard metrics and recent activity are illustrative placeholders, and task submission, workflow persistence, drag-and-drop, and real workflow execution are not yet connected to backend APIs. UI copy explicitly indicates this where relevant. Never use preview metrics as operational truth.

The existing secure FastAPI application remains under `backend/`. This frontend is a separate app and does not silently replace the current API-served UI. Backend integration and deployment are follow-up work after visual review and frontend checks.
