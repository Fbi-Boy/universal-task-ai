#!/usr/bin/env python3
"""Bounded local HTTP smoke test for the authenticated application surface."""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def request(url: str, *, token: str | None = None) -> tuple[int, object]:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urlopen(Request(url, headers=headers), timeout=5) as response:
            body = response.read(64 * 1024)
            return response.status, json.loads(body or b"{}")
    except HTTPError as exc:
        return exc.code, exc.read(64 * 1024).decode("utf-8", errors="replace")
    except URLError as exc:
        raise SystemExit(f"smoke test connection failed: {exc}") from exc


def main() -> int:
    base = os.environ.get("UTA_SMOKE_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    token = os.environ.get("UNIVERSAL_TASK_AI_API_KEY")
    if not token:
        print("UNIVERSAL_TASK_AI_API_KEY is required for authenticated smoke tests.", file=sys.stderr)
        return 2

    status, payload = request(f"{base}/health")
    if status != 200 or not isinstance(payload, dict) or payload.get("status") != "ok":
        print(f"health check failed: status={status} payload={payload}", file=sys.stderr)
        return 3

    status, _ = request(f"{base}/v1/tools")
    if status != 401:
        print(f"auth boundary failed: unauthenticated /v1/tools returned {status}", file=sys.stderr)
        return 4

    status, payload = request(f"{base}/v1/tools", token=token)
    if status != 200 or not isinstance(payload, list):
        print(f"authenticated tool catalog failed: status={status} payload={payload}", file=sys.stderr)
        return 5

    print("smoke_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
