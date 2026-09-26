# Durable Channel Idempotency

Inbound channel deduplication can span process restarts by using SQLite. Claims are atomic through a primary-key constraint, keys and result identifiers are bounded, and expired records are removed before a new claim.

The store is deliberately limited to deduplication state; it does not authorize an action. Authorization, approval, audit, and normal task dispatch remain separate controls.
