import pytest

from backend.core.budget import BudgetExceeded, BudgetTracker, ExecutionBudget
from backend.core.router import choose_route
from backend.core.schemas import TaskContract

def test_router_sends_required_tools_to_tool_route():
    task = TaskContract(goal="search", tools_required=["web_search"], tools_allowed=["web_search"])
    assert choose_route(task).kind == "tool"

def test_router_requires_approval_for_risky_task():
    task = TaskContract(goal="publish", risk_level="critical", approval_required=True)
    assert choose_route(task).kind == "clarification"

def test_budget_blocks_excess_turns():
    tracker = BudgetTracker(ExecutionBudget(max_turns=1))
    tracker.consume_turn()
    with pytest.raises(BudgetExceeded):
        tracker.consume_turn()

def test_budget_blocks_excess_tool_calls():
    tracker = BudgetTracker(ExecutionBudget(max_tool_calls=1))
    tracker.consume_tool_call()
    with pytest.raises(BudgetExceeded):
        tracker.consume_tool_call()

def test_invalid_budget_is_rejected():
    with pytest.raises(ValueError):
        BudgetTracker(ExecutionBudget(max_turns=0))
