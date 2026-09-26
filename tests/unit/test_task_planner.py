from backend.core.schemas import TaskContract
from backend.core.task_planner import TaskPlanner

def test_planner_builds_safe_baseline_for_simple_task():
    plan = TaskPlanner().plan(TaskContract(goal="Create a report"))
    assert [step.kind for step in plan.steps] == ["analyze", "finalize"]
    assert plan.steps[-1].depends_on == ["analyze"]

def test_planner_marks_required_tools_explicitly():
    plan = TaskPlanner().plan(TaskContract(goal="Search", tools_required=["web.search"]))
    assert [step.kind for step in plan.steps] == ["analyze", "tool", "finalize"]
    assert plan.steps[1].required_tools == ["web.search"]
