from uuid import uuid4

from backend.core.analyzer import TaskAnalysis
from backend.core.planner import ExecutionPlan, PlanStep
from backend.core.plan_validation import validate_execution_plan
from backend.core.requirement_extractor import extract_requirements

def test_requirement_extractor_preserves_bulleted_requirements():
    result = extract_requirements("- search docs\n- summarize findings")
    assert [item.description for item in result.items] == ["search docs", "summarize findings"]

def test_analyzer_marks_vague_task_as_high_ambiguity():
    result = TaskAnalysis.from_task_text("terserah, buat sesuatu")
    assert result.ambiguity_level == "high"
    assert result.needs_clarification is True

def test_analyzer_marks_preference_language_as_medium():
    result = TaskAnalysis.from_task_text("buat desain yang bagus untuk produk ini")
    assert result.ambiguity_level == "medium"
    assert result.needs_clarification is False

def test_plan_rejects_unknown_dependency():
    plan = ExecutionPlan(
        task_id=uuid4(),
        steps=[
            PlanStep(step_id="step_1", kind="analyze", objective="analyze", depends_on=["missing"]),
        ],
        max_turns=1,
    )
    result = validate_execution_plan(plan)
    assert result.passed is False
    assert any("unknown steps" in error for error in result.errors)

def test_plan_rejects_dependency_cycle():
    plan = ExecutionPlan(
        task_id=uuid4(),
        steps=[
            PlanStep(step_id="a", kind="analyze", objective="a", depends_on=["b"]),
            PlanStep(step_id="b", kind="review", objective="b", depends_on=["a"]),
        ],
        max_turns=2,
    )
    result = validate_execution_plan(plan)
    assert result.passed is False
    assert any("cycle" in error for error in result.errors)

def test_valid_plan_passes():
    plan = ExecutionPlan(
        task_id=uuid4(),
        steps=[
            PlanStep(step_id="analyze", kind="analyze", objective="analyze"),
            PlanStep(
                step_id="finalize",
                kind="finalize",
                objective="finalize",
                depends_on=["analyze"],
            ),
        ],
        max_turns=2,
    )
    assert validate_execution_plan(plan).passed
