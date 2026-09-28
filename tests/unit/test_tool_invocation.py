import math

import pytest
from pydantic import ValidationError

from backend.core.tool_invocation import ToolInvocation


def test_tool_invocation_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        ToolInvocation(tool_name="x", arguments={}, approved=True)


def test_tool_invocation_bounds_top_level_keys() -> None:
    invocation = ToolInvocation(tool_name="x", arguments={str(i): i for i in range(33)})
    with pytest.raises(ValueError):
        invocation.validate_bounds()


def test_tool_invocation_bounds_depth() -> None:
    value = {}
    current = value
    for _ in range(10):
        current["x"] = {}
        current = current["x"]
    invocation = ToolInvocation(tool_name="x", arguments=value)
    with pytest.raises(ValueError):
        invocation.validate_bounds()


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_tool_invocation_rejects_non_finite_numbers(value: float) -> None:
    invocation = ToolInvocation(tool_name="x", arguments={"value": value})
    with pytest.raises(ValueError, match="non-finite"):
        invocation.validate_bounds()


def test_tool_invocation_rejects_non_json_python_objects() -> None:
    invocation = ToolInvocation(tool_name="x", arguments={"value": object()})
    with pytest.raises(ValueError, match="JSON-compatible"):
        invocation.validate_bounds()


def test_tool_invocation_rejects_non_string_object_keys() -> None:
    invocation = ToolInvocation(tool_name="x", arguments={"nested": {1: "value"}})
    with pytest.raises(ValueError, match="keys must be strings"):
        invocation.validate_bounds()


def test_tool_invocation_bounds_aggregate_string_bytes() -> None:
    invocation = ToolInvocation(
        tool_name="x",
        arguments={"a": "x" * (64 * 1024), "b": "y" * (64 * 1024),
                   "c": "z" * (64 * 1024), "d": "q" * (64 * 1024)},
    )
    with pytest.raises(ValueError, match="aggregate string size"):
        invocation.validate_bounds()


def test_tool_invocation_rejects_huge_integer() -> None:
    invocation = ToolInvocation(tool_name="x", arguments={"value": 1 << 300})
    with pytest.raises(ValueError, match="integer"):
        invocation.validate_bounds()
