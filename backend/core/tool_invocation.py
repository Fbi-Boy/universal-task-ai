from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field


class ToolInvocation(BaseModel):
    """Bounded, explicit request to invoke one registered runtime tool."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = Field(min_length=1, max_length=128)
    arguments: Mapping[str, Any] = Field(default_factory=dict)

    def validate_bounds(self) -> None:
        if len(self.arguments) > 32:
            raise ValueError("tool arguments are limited to 32 top-level keys")
        for key in self.arguments:
            if not isinstance(key, str) or len(key) > 128:
                raise ValueError("tool argument keys must be strings of at most 128 characters")
        if _nested_size(self.arguments) > 256:
            raise ValueError("tool arguments exceed the maximum nested value count")


def _nested_size(value: Any, *, depth: int = 0) -> int:
    if depth > 8:
        raise ValueError("tool arguments exceed maximum nesting depth")
    if isinstance(value, Mapping):
        return 1 + sum(
            _nested_size(k, depth=depth + 1) + _nested_size(v, depth=depth + 1)
            for k, v in value.items()
        )
    if isinstance(value, (list, tuple)):
        return 1 + sum(_nested_size(item, depth=depth + 1) for item in value)
    if isinstance(value, (str, bytes)) and len(value) > 64 * 1024:
        raise ValueError("tool argument value exceeds 64 KiB")
    return 1
