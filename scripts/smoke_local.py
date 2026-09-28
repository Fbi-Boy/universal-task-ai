#!/usr/bin/env python3
"""Bounded local HTTP smoke test for the authenticated application surface.

The API key is only sent to an explicitly loopback base URL. This prevents a
mistyped or hostile UTA_SMOKE_BASE_URL from receiving the local credential.
"""

from __future__ import annotations

import ipaddress
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen



def validate_base_url(raw: str) -> str:
    """Accept only an HTTP(S) loopback URL with no embedded credentials/query."""
    if not raw or raw != raw.strip() or any(ord(char) < 33 for char in raw):
        raise ValueError("smoke test base URL must be a clean loopback URL")
    try:
        parsed = urlsplit(raw)
        port = parsed.port
    except ValueError as exc:
        raise ValueError("smoke test base URL is invalid") from exc

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("smoke test base URL must use HTTP or HTTPS")
    host = parsed.hostname
    if host is None or "%" in host:
        raise ValueError("smoke test refuses non-loopback destinations")
    try:
        address = ipaddress.ip_address(host)
    except ValueError as exc:
        raise ValueError("smoke test requires a literal loopback IP address") from exc
    if not address.is_loopback or str(address) != host.lower():
        raise ValueError("smoke test refuses non-loopback destinations")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("smoke test base URL must not contain credentials")
    if parsed.query or parsed.fragment:
        raise ValueError("smoke test base URL must not contain a query or fragment")
    if port is not None and not 1 <= port <= 65535:
        raise ValueError("smoke test port is out of range")
    return raw.rstrip("/")


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
    try:
        base = validate_base_url(
            os.environ.get("UTA_SMOKE_BASE_URL", "http://127.0.0.1:8000")
        )
    except ValueError as exc:
        print(f"invalid smoke test destination: {exc}", file=sys.stderr)
        return 2

    token = os.environ.get("UNIVERSAL_TASK_AI_API_KEY")
    if not token:
        print(
            "UNIVERSAL_TASK_AI_API_KEY is required for authenticated smoke tests.",
            file=sys.stderr,
        )
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
