import pytest
from pydantic import ValidationError

from backend.core.schemas import TaskContract
from backend.core.validation import validate_task_contract, validate_output_schema

def test_required_tool_must_be_allowed():
    task = TaskContract(
        goal="inspect",
        tools_required=["file_reader"],
        tools_allowed=[],
    )
    result = validate_task_contract(task)
    assert result.passed is False
    assert "file_reader" in result.errors[0]

def test_high_risk_requires_approval():
    task = TaskContract(goal="delete data", risk_level="high")
    result = validate_task_contract(task)
    assert result.passed is False

def test_high_risk_with_approval_passes():
    task = TaskContract(goal="delete data", risk_level="high", approval_required=True)
    assert validate_task_contract(task).passed

def test_extra_fields_are_rejected():
    with pytest.raises(ValidationError):
        TaskContract(goal="x", unexpected="value")

def test_blank_list_items_are_rejected():
    with pytest.raises(ValidationError):
        TaskContract(goal="x", constraints=[" "])

def test_output_validation_rejects_none():
    assert validate_output_schema(None).passed is False
