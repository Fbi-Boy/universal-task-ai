# Notification Event Router

The router is a transport-neutral boundary for user notifications.

Security:
- Only validated run/user identifiers are accepted.
- Message size is bounded.
- Adapters remain responsible for channel-specific authentication and transport security.
- Notification dispatch never grants task permissions and never resumes a task by itself.
- Approval-required notifications must contain a reference to the existing approval flow; the message itself is not authorization.
