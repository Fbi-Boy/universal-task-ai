# Programming Workspace Context

The programming assistant may read project context only through an explicit workspace policy.

Controls:
- roots are configured explicitly; paths outside them are denied;
- symlink paths and symlink targets are rejected;
- only bounded source/configuration extensions are collected by default;
- Git metadata, virtual environments, dependency trees, and caches are excluded;
- file count and file size are bounded;
- this capability is read-only and never invokes a shell, process, browser, or network operation.

The runtime tool is named filesystem.project_context, so the runtime filesystem capability gate remains authoritative.

Secrets should not be stored in project source files. Future secret-aware scanning must be a separate security boundary and must not silently expand file access.
