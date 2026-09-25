from threading import Lock
from uuid import UUID

from backend.core.approval import ApprovalMachine, ApprovalRequest


class ApprovalStore:
    """In-memory approval store with atomic state transitions."""

    def __init__(self, machine: ApprovalMachine | None = None) -> None:
        self._machine = machine or ApprovalMachine()
        self._lock = Lock()
        self._requests: dict[UUID, ApprovalRequest] = {}

    def create(self, task_id: UUID, action: str) -> ApprovalRequest:
        request = self._machine.request(task_id, action)
        with self._lock:
            self._requests[request.approval_id] = request
        return request

    def get(self, approval_id: UUID) -> ApprovalRequest | None:
        with self._lock:
            return self._requests.get(approval_id)

    def approve(self, approval_id: UUID) -> ApprovalRequest:
        with self._lock:
            current = self._requests.get(approval_id)
            if current is None:
                raise KeyError("approval not found")
            updated = self._machine.approve(current)
            self._requests[approval_id] = updated
            return updated

    def reject(self, approval_id: UUID) -> ApprovalRequest:
        with self._lock:
            current = self._requests.get(approval_id)
            if current is None:
                raise KeyError("approval not found")
            updated = self._machine.reject(current)
            self._requests[approval_id] = updated
            return updated
