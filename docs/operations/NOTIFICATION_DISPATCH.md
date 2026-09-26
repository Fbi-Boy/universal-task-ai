# Notification Dispatch

Notification routing is explicit by event kind. An adapter receives an event only when a matching route is configured. Unknown or unconfigured event kinds fail closed instead of broadcasting to every channel.

Adapters remain responsible for their transport-level authentication and secret handling.
