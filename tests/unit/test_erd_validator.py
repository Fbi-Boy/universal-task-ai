from backend.core.erd_validator import ERDValidator

def test_erd_validator_rejects_empty():
    assert not ERDValidator().validate("").passed

def test_erd_validator_accepts_basic_schema():
    assert ERDValidator().validate("User(id PK) -> Order(user_id FK)").passed
