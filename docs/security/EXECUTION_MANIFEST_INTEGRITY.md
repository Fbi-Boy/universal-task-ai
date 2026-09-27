# Execution Manifest Integrity

Approval-gated execution persists a canonical SHA-256 fingerprint for the task contract and execution plan.

## Boundary

Before an approved execution is consumed:

1. The durable waiting run is reconstructed.
2. The current contract and plan are canonicalized and hashed.
3. The approval store compares both hashes with the values captured before approval.
4. Only an exact match may consume the approval.
5. Capability authorization is still re-run immediately before tool execution.

A changed manifest fails closed and does not consume the approval.

## Migration

Existing SQLite approval databases are upgraded in place with nullable integrity columns. No destructive reset or data loss is required.

## Threat model

The hashes protect against cross-layer state drift or accidental/tampered manifest substitution between approval creation and resume. They do not replace filesystem/database permissions, authentication, authorization, or encrypted storage.
