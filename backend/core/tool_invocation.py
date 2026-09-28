import math
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field


class ToolInvocation(BaseModel):
    """Bounded, explicit request to invoke one registered runtime tool."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = Field(min_length=1, max_length=128)
    arguments: Mapping[str, Any] = Field(default_factory=dict)

    def validate_bounds(self) -> None:
        """Reject non-JSON values and bound the complete argument tree.

        This check is deliberately performed immediately before tool execution,
        because internal callers can construct models without going through the
        HTTP JSON parser.
        """
        if not isinstance(self.arguments, Mapping):
            raise ValueError("tool arguments must be a JSON object")
        if len(self.arguments) > 32:
            raise ValueError("tool arguments are limited to 32 top-level keys")

        budget = {"nodes": 0, "string_bytes": 0}
        _validate_json_value(self.arguments, depth=0, budget=budget)
        if budget["nodes"] > 256:
            raise ValueError("tool arguments exceed the maximum nested value count")
        if budget["string_bytes"] > 256 * 1024:
            raise ValueError("tool arguments exceed the maximum aggregate string size")


def _validate_json_value(value: Any, *, depth: int, budget: dict[str, int]) -> None:
    if depth > 8:
        raise ValueError("tool arguments exceed maximum nesting depth")

    budget["nodes"] += 1
    if budget["nodes"] > 256:
        raise ValueError("tool arguments exceed the maximum nested value count")

    if value is None or isinstance(value, bool):
        return
    if isinstance(value, str):
        size = len(value.encode("utf-8"))
        if size > 64 * 1024:
            raise ValueError("tool argument value exceeds 64 KiB")
        budget["string_bytes"] += size
        return
    if isinstance(value, int):
        if value.bit_length() > 256:
            raise ValueError("tool integer exceeds the supported numeric bound")
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("tool arguments must not contain non-finite numbers")
        return
    if isinstance(value, Mapping):
        if len(value) > 32 and depth == 0:
            raise ValueError("tool arguments are limited to 32 top-level keys")
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("tool argument object keys must be strings")
            key_size = len(key.encode("utf-8"))
            if key_size > 128:
                raise ValueError("tool argument keys must be at most 128 UTF-8 bytes")
            budget["string_bytes"] += key_size
            _validate_json_value(item, depth=depth + 1, budget=budget)
        return
    if isinstance(value, list):
        for item in value:
            _validate_json_value(item, depth=depth + 1, budget=budget)
        return
    raise ValueError("tool arguments must contain only JSON-compatible values")
