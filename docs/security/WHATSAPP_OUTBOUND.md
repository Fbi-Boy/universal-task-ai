# WhatsApp Outbound Boundary

Outbound delivery is an adapter only. It does not execute tasks, grant permissions, approve actions, or mutate task state. Credentials belong in SecretProvider and provider errors must not leak secrets into logs.