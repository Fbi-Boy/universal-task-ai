from __future__ import annotations

import os

VERSION = "0.1.0"


def build_version() -> str:
    return os.environ.get("UTA_BUILD_VERSION", VERSION).strip() or VERSION


def build_sha() -> str:
    return os.environ.get("UTA_BUILD_SHA", "unknown").strip() or "unknown"
