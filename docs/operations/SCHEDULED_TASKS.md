# Scheduled Tasks

Scheduled tasks are triggers, not a second execution engine. A scheduler creates
an ordinary task dispatch, which then follows the same planner, router, tool
permissions, approvals, execution, audit, and reviewer pipeline as an
interactive request.

## Supported primitives

- one-time timezone-aware execution
- bounded recurring interval definition
- per-user ownership
- explicit enabled state

The first implementation intentionally does not support arbitrary cron strings.
Cron parsing and persistent schedule storage will be added only with validation,
timezone handling, missed-run policy, idempotency, and regression coverage.

## Future channels

The same dispatch pipeline is designed to accept triggers from the web UI,
WhatsApp webhook, email, calendar, or other approved integrations. A channel
must authenticate the sender and map the message to a user before dispatching.

A scheduled task never bypasses normal approvals or tool permissions.
