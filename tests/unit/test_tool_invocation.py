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
