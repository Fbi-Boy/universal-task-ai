# Audit metadata redaction

Audit records are security-relevant and may contain data derived from untrusted task input. Before persistence or export, `AuditEvent.safe_metadata()` recursively removes fields whose names indicate credentials, tokens, keys, authorization headers, cookies, or passwords. Matching handles common snake_case, kebab-case, and camelCase variants.

The sanitizer also bounds nesting depth, mapping/collection size, and scalar size. Keep audit metadata small and descriptive: do not include raw tool arguments, request bodies, credentials, or user file contents. Redaction is a defense-in-depth control, not permission to place secrets in metadata.

Tests cover nested secret-key variants, preservation of ordinary diagnostic fields, and size/depth limits.
