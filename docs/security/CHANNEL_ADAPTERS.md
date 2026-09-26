# Channel Adapter Security Contract

Adapters translate external messages into the universal task engine. They do not execute tools.

Inbound processing must authenticate the external request, map the sender to an internal user identity, reject unauthenticated commands, and preserve a stable reply target. Outbound messages must be bound to the authenticated internal user/channel mapping.

A WhatsApp adapter must verify the provider webhook signature and verification challenge, apply replay protection/rate limits, use the SecretProvider for credentials, and never treat message content as permission. Interactive commands continue through the same task planner, permission broker, approval service, audit events, reviewer, and finalizer.

Approval messages must identify the pending task/action without exposing credentials or secrets.
