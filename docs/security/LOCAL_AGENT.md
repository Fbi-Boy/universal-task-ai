# Local Agent Security Boundary

The local agent is a capability broker, not a general-purpose shell.

## Initial capability

V1 starts with one explicitly named capability: `filesystem.read_text`.
The broker requires configured filesystem roots, rejects symlink paths, enforces
root containment after resolution, limits file size, and only decodes UTF-8 text.

## Non-goals

The broker does not grant arbitrary shell execution, filesystem writes, process
creation, desktop control, credential access, or network access. Each future
capability must be added explicitly with its own permission, threat-model
review, regression tests, and documentation.

## Design rule

A model request must never turn an untrusted path or operation name into
implicit local authority. The broker validates the capability and path before
performing any local operation.
