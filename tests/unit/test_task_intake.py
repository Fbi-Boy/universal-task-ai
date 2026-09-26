import pytest
from backend.core.task_intake import TaskIntakeService

def test_intake_builds_contract_from_user_text():
    result = TaskIntakeService().intake("Create a report")
    assert result.contract.goal == "Create a report"
    assert result.contract.constraints == ["Create a report"]

def test_intake_rejects_empty_text():
    with pytest.raises(ValueError):
        TaskIntakeService().intake("   ")
