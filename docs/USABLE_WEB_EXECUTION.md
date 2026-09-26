# Web Task Execution

The web UI can now execute the same bounded runtime used by the API.

## Setup

1. Configure `UNIVERSAL_TASK_AI_API_KEY`.
2. Start the FastAPI application.
3. Open the web UI.
4. Enter the API key in the **Connection** panel. It is kept only in `sessionStorage` for the current browser session.
5. Select an allowlisted tool when needed and provide its JSON arguments.
6. Click **Run task**.
7. If the selected tool requires approval, approve it from **Pending approvals**. The UI then resumes the exact waiting run using the server-side approval manifest.

## Capability examples

- `calculator`: `{"expression":"12 * 8"}`
- `filesystem.read_text`: `{"path":"relative/path.txt"}` when `UTA_LOCAL_ROOTS` is configured.
- `filesystem.project_context`: `{"paths":["backend/core/task_executor.py"]}` when a workspace root is configured.
- `browser_worker`: use an explicit browser action and HTTPS allowlisted URL when browser capability is enabled.

The server remains authoritative. The UI cannot grant a capability that is not present in the runtime boundary.

## Security

- The API key is never inserted into task text or tool arguments.
- Tool metadata is exposed read-only; invocation authorization remains server-side.
- Approval execution metadata does not expose persisted invocation arguments.
- Browser and other approval-required tools remain blocked until approval is consumed.
- Local capability remains explicitly rooted and read-only.
