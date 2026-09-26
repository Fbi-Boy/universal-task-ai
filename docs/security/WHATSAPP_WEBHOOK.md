# WhatsApp Webhook Security

Inbound webhook requests must pass provider signature verification before parsing commands. Verification secrets come from SecretProvider and are never included in logs.

The verification challenge is checked with constant-time comparison. Invalid signatures/challenges are rejected before user identity mapping or task dispatch.

After authentication, the adapter maps the provider sender to an internal user identity. Message text never grants permissions. Rate limiting, replay protection, audit events, and the existing approval pipeline remain mandatory before production rollout.
