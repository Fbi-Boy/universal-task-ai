from backend.core.flowchart_structural_validator import FlowchartStructuralValidator

def test_flowchart_structure():
    v=FlowchartStructuralValidator()
    assert not v.validate("Process -> END").passed
    assert v.validate("START -> Process -> END").passed
