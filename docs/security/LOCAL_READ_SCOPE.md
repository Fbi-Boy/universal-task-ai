# Local Read Scope

This boundary extends the local agent with read-only file listing and text reads inside one resolved root.

Security:
- No writes, shell execution, process creation, or network access.
- Paths are resolved and contained before filesystem access.
- NUL bytes and symlinks are rejected.
- File size is bounded.
- Callers must still pass the existing local capability policy; this class is not an authorization grant.
