import pytest

from backend.core.approval import ApprovalMachine, ApprovalState
from backend.core.idempotency import IdempotencyStore
from backend.core.reliability import FailureKind, RetryPolicy, classify_failure
from backend.core.validators import all_passed, validate_required_fields


class TimeoutErrorForTest(Exception):
    pass


def test_failure_classification() -> None:
    assert classify_failure(ValueError("bad")).kind is FailureKind.VALIDATION
    assert classify_failure(TimeoutErrorForTest("slow")).kind is FailureKind.TIMEOUT


def test_retry_policy_retries_transient_timeout() -> None:
    attempts = 0
    def operation() -> int:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise TimeoutErrorForTest("slow")
        return 7
    assert RetryPolicy(3).run(operation) == 7
    assert attempts == 3


def test_validators_are_deterministic() -> None:
    checks = validate_required_fields({"a": 1}, ["a", "b"])
    assert not all_passed(checks)


def test_approval_transitions() -> None:
    task_id = __import__("uuid").uuid4()
    machine = ApprovalMachine()
    request = machine.request(task_id, "publish")
    approved = machine.approve(request)
    assert approved.state is ApprovalState.APPROVED
    with pytest.raises(ValueError):
        machine.approve(approved)


def test_idempotency_put_once() -> None:
    store = IdempotencyStore()
    assert store.put_once("k", 1)
    assert not store.put_once("k", 2)
    assert store.get("k") == 1
