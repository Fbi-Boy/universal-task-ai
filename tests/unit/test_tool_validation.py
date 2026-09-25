import pytest

from backend.core.tool_validation import ToolCall, validate_tool_result
from backend.core.tools import ToolResult


def test_tool_call_rejects_unknown_fields() -> None:
    with pytest.raises(ValueError):
        ToolCall(tool_name="calculator", arguments={}, admin=True)


def test_success_result_cannot_have_error() -> None:
    with pytest.raises(ValueError):
        validate_tool_result(ToolResult(success=True, output=1, error="bad"))


def test_failed_result_requires_error() -> None:
    with pytest.raises(ValueError):
        validate_tool_result(ToolResult(success=False))


def test_valid_result_passes() -> None:
    result = ToolResult(success=True, output=42)
    assert validate_tool_result(result) == result
