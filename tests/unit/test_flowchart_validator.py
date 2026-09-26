from backend.core.flowchart_validator import FlowchartValidator

def test_flowchart_requires_start_end_and_transition():
    assert not FlowchartValidator().validate("A -> B").passed
    assert FlowchartValidator().validate("START -> Process -> END").passed
