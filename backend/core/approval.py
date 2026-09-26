from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID, uuid4


class ApprovalState(StrEnum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CONSUMED = "consumed"


@dataclass(frozen=True)
class ApprovalRequest:
    approval_id: UUID
    task_id: UUID
    action: str
    state: ApprovalState = ApprovalState.PENDING

    def __post_init__(self) -> None:
        if not str(self.action).strip():
            raise ValueError("action must not be empty")


class ApprovalMachine:
    def request(self, task_id: UUID, action: str) -> ApprovalRequest:
        return ApprovalRequest(uuid4(), task_id, action.strip())

    def approve(self, request: ApprovalRequest) -> ApprovalRequest:
        if request.state is not ApprovalState.PENDING:
            raise ValueError("only pending approvals can be approved")
        return ApprovalRequest(request.approval_id, request.task_id, request.action, ApprovalState.APPROVED)

    def reject(self, request: ApprovalRequest) -> ApprovalRequest:
        if request.state is not ApprovalState.PENDING:
            raise ValueError("only pending approvals can be rejected")
        return ApprovalRequest(request.approval_id, request.task_id, request.action, ApprovalState.REJECTED)

    def consume(self, request: ApprovalRequest) -> ApprovalRequest:
        if request.state is not ApprovalState.APPROVED:
            raise ValueError("only approved approvals can be consumed")
        return ApprovalRequest(request.approval_id, request.task_id, request.action, ApprovalState.CONSUMED)
