from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_sha256(value: Any) -> str:
    """Hash a JSON-compatible manifest with deterministic serialization."""
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def contract_hash(contract: Any) -> str:
    return canonical_sha256(contract.model_dump(mode="json"))


def plan_hash(plan: Any) -> str:
    return canonical_sha256(plan.model_dump(mode="json"))
