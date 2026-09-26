# Browser Execution Boundary

A browser session holds only browser state and the current policy. Every initial navigation and redirect is revalidated against the host policy.

## Supported worker actions

The Playwright worker supports only:

- navigate — HTTPS navigation to an explicitly allowlisted host.
- read — bounded text extraction from the current page or a bounded selector.
- click — click an explicit selector.
- type — fill an explicit selector with a value capped at 64 KiB.
- submit — click an explicit submit selector and revalidate the resulting URL.

The browser tool remains high-risk, network-capable, and approval-required through RuntimeToolBoundary, so these actions cannot run merely because a caller can name the tool.

upload, download, login, and payment remain deliberately unimplemented. They require additional capability-specific controls rather than being silently enabled by the generic browser worker.

## Security controls

- HTTPS only and explicit host allowlist.
- Credentials in URLs are rejected.
- Every browser request is intercepted and revalidated.
- Redirect destinations are revalidated.
- Downloads are disabled in the Playwright context.
- Selectors are bounded to 2 KiB and typed values to 64 KiB.
- Browser output is bounded to 256,000 characters by default.
- The worker uses an ephemeral headless browser context.
- The production executor must run in an isolated browser/container with bounded CPU, memory, time, and filesystem access.
- Credentials must not be persisted in ordinary task state.
- Sensitive actions must pause for explicit user approval and emit audit events before resuming.
