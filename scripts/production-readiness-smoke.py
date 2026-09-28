#!/usr/bin/env python3
"""Fail-closed, non-destructive smoke checks for a production-like stack."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "http://127.0.0.1:8000"
API_KEY_PATH = Path("secrets/universal_task_ai_api_key")


def request(path: str, *, method: str = "GET", payload: dict | None = None, api_key: str | None = None):
    headers = {"Accept": "application/json"}
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    if api_key is not None:
        headers["Authorization"] = f"Bearer {api_key}"
    req = Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=5) as response:
            body = response.read(64 * 1024 + 1)
            if len(body) > 64 * 1024:
                raise RuntimeError("smoke response exceeded 64 KiB")
            return response.status, json.loads(body) if body else {}
    except HTTPError as exc:
        body = exc.read(4096)
        try:
            decoded = json.loads(body) if body else {}
        except (ValueError, UnicodeDecodeError):
            decoded = {}
        return exc.code, decoded
    except (URLError, TimeoutError) as exc:
        raise RuntimeError(f"deployment smoke request failed for {path}") from exc


def main() -> None:
    status, health = request("/health")
    if status != 200 or health.get("status") != "ok":
        raise SystemExit("FAIL: health endpoint did not report healthy")

    status, readiness = request("/ready")
    if status != 200:
        detail = readiness.get("detail", "no safe diagnostic returned")
        raise SystemExit(f"FAIL: readiness endpoint returned HTTP {status}: {detail}")
    if readiness.get("status") != "ready":
        raise SystemExit("FAIL: readiness endpoint returned an unexpected status")
    for dependency in ("run_state", "approval_store", "audit_sink"):
        if readiness.get(dependency) != "ok":
            raise SystemExit(f"FAIL: readiness dependency check failed: {dependency}")

    status, _ = request("/v1/tasks", method="POST", payload={"task": "smoke test"})
    if status != 401:
        raise SystemExit("FAIL: protected task endpoint did not reject missing authentication")

    try:
        api_key = API_KEY_PATH.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit("FAIL: smoke API key file is unavailable") from exc
    if not api_key or len(api_key) > 4096:
        raise SystemExit("FAIL: smoke API key is empty or invalid")

    status, task = request(
        "/v1/tasks",
        method="POST",
        payload={"task": "Verify the task runtime is responsive without using external tools."},
        api_key=api_key,
    )
    if status != 200 or task.get("status") != "succeeded":
        raise SystemExit("FAIL: authenticated low-risk task smoke test did not succeed")

    print("PASS: health, durable readiness, auth rejection, and authenticated low-risk task")


if __name__ == "__main__":
    main()
