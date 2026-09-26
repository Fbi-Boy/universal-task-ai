# Local and Browser Capability Boundary

## Local filesystem

The runtime exposes local files only as filesystem.read_text. The capability is disabled unless explicit local roots are configured. The broker rejects parent traversal, symlink escapes, non-files, oversized files, and every operation other than UTF-8 text reads. It never invokes a shell or arbitrary process.

Configure local roots with UTA_LOCAL_ROOTS as an OS-specific path-separated list. Keep roots narrow.

## Browser

The optional Playwright worker is disabled by default. When enabled it uses an ephemeral headless browser context, HTTPS-only navigation, an explicit host allowlist, request interception, redirect revalidation, bounded text output, and no downloads. Only navigate and read are implemented initially. Click/type/upload/submit/login/payment remain denied until their approval and side-effect contracts are separately reviewed.

Browser execution remains an approval-required, network-capable tool. Approval is consumed by the durable approval state machine before the worker is reached.

## Configuration

- UTA_LOCAL_ROOTS: optional local read roots.
- UTA_BROWSER_ENABLED=true: opt into the browser worker.
- UTA_BROWSER_ALLOWED_HOSTS: comma-separated HTTPS host allowlist.

Never place credentials in browser URLs or task arguments. Secrets belong in the secret provider, not tool invocation payloads.
