#!/usr/bin/env python3
"""Fail-closed checks for a real production rollout."""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys

REQUIRED_ENV = ("DEPLOY_HOST", "DEPLOY_USER", "DEPLOY_PATH", "DEPLOY_SSH_KEY", "DEPLOY_KNOWN_HOSTS")
DIGEST = re.compile(r"^ghcr\.io/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@sha256:[0-9a-f]{64}$")


def main() -> int:
    missing = [key for key in REQUIRED_ENV if not os.environ.get(key, "").strip()]
    if missing:
        print("missing deployment configuration: " + ", ".join(missing), file=sys.stderr)
        return 2

    image = os.environ.get("UTA_IMAGE", "").strip()
    if not DIGEST.fullmatch(image):
        print("UTA_IMAGE must be an immutable GHCR sha256 digest.", file=sys.stderr)
        return 3

    known_hosts = Path(os.environ["DEPLOY_KNOWN_HOSTS"])
    if not known_hosts.is_file() or known_hosts.stat().st_size == 0:
        print("DEPLOY_KNOWN_HOSTS must point to a non-empty known-hosts file.", file=sys.stderr)
        return 4

    print("production_preflight_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
