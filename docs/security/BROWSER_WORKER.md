# Browser Worker Security Contract

The browser worker is an isolated capability, not a general-purpose network client.

Required controls before production:
- HTTPS and explicit host allowlist.
- Revalidate every navigation and redirect.
- Isolated browser profile/container and bounded resources.
- Downloads stored in an isolated artifact area with size/type limits.
- No credentials in URLs or ordinary task logs.
- Web content is untrusted input and cannot modify permissions.
- Login, credential entry, upload, submit, purchase/payment, and configured external side effects pause for human approval.
- Every browser action emits an audit event.
- Browser failure cannot silently fall back to local shell execution.

The first implementation may use Playwright, but the worker must remain behind this policy and the existing permission/approval/audit/reviewer pipeline.
