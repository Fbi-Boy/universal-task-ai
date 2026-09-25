from uuid import uuid4

from backend.api.approval import approve, create_approval, get_approval, reject, store, ApprovalCreate


def test_approval_api_lifecycle() -> None:
    created = create_approval(ApprovalCreate(task_id=uuid4(), action="run sandbox"))
    assert created.state.value == "pending"
    assert get_approval(created.approval_id) == created
    approved = approve(created.approval_id)
    assert approved.state.value == "approved"


def test_reject_lifecycle() -> None:
    created = create_approval(ApprovalCreate(task_id=uuid4(), action="publish"))
    rejected = reject(created.approval_id)
    assert rejected.state.value == "rejected"
