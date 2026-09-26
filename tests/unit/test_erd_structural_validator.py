from backend.core.erd_structural_validator import ERDStructuralValidator

def test_erd_structure():
    assert not ERDStructuralValidator().validate("table User\nid name").passed
    assert ERDStructuralValidator().validate("table User\nid PK\nuser_id FK").passed
