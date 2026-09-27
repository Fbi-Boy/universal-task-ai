# Browser Execution Boundary

Browser execution is high-risk and network-capable. It is available only through the runtime capability boundary and requires approval.

## Supported worker actions

The Playwright worker supports navigate, read, click, type, and submit. Upload, download, login, and payment remain deliberately unimplemented.

A single invocation may contain a bounded batch of up to 8 commands. This is the supported way to keep browser state across multiple actions such as navigate -> read/click/type while preserving task-level isolation.

## Security controls

- HTTPS only and explicit host allowlist.
- Credentials in URLs are rejected.
- Every browser request is intercepted and revalidated.
- Redirect destinations are revalidated.
- Downloads are disabled in the Playwright context.
- Selectors are bounded to 2 KiB and typed values to 64 KiB.
- Browser output is bounded to 256,000 characters by default.
- Each tool invocation gets a fresh browser context and is closed in a finally block; cookies, storage, and page state are not reused across invocations.
- Multi-action browser work stays within one bounded batch rather than sharing a context between tasks.
- Browser actions are revalidated against the current URL after navigation, click, submit, and type.
- The production executor must run in an isolated browser/container with bounded CPU, memory, time, and filesystem access.
- Credentials must not be persisted in ordinary task state.
- Sensitive actions pause for explicit user approval and emit audit events before resuming.
