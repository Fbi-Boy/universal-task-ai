# Scheduler Worker

The worker is a trigger, not an execution engine. It claims due schedules, then dispatches the stored task payload into the universal task pipeline.

Safety properties:
- UTC-normalized timestamps.
- Persistent idempotent claims prevent duplicate concurrent dispatch for the same schedule.
- Tool permissions, approvals, audit, reviewer, and finalization remain downstream.
- A failed dispatch releases the claim so it can be retried.
- The worker never executes browser, local, shell, or network tools directly.
