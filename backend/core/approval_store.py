import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from uuid import UUID

from backend.core.approval import ApprovalMachine, ApprovalRequest, ApprovalState
from backend.core.tool_invocation import ToolInvocation


@dataclass(frozen=True)
class ApprovalExecution:
    request: ApprovalRequest
    run_id: str
    plan_id: UUID
    invocations: tuple[ToolInvocation, ...]


class ApprovalStore:
    """SQLite-backed approval store with atomic approval consumption.

    The default in-memory database preserves isolated unit-test behavior.
    Production callers should provide a persistent path.
    """

    def __init__(self, path: Path | str = ":memory:", machine: ApprovalMachine | None = None) -> None:
        self._machine = machine or ApprovalMachine()
        self._lock = Lock()
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS approvals (
                approval_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                action TEXT NOT NULL,
                state TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS approval_executions (
                approval_id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL UNIQUE,
                plan_id TEXT NOT NULL,
                invocations TEXT NOT NULL,
                FOREIGN KEY(approval_id) REFERENCES approvals(approval_id)
            )
            """
        )
        self._conn.commit()

    def create(self, task_id: UUID, action: str) -> ApprovalRequest:
        request = self._machine.request(task_id, action)
        with self._lock:
            self._conn.execute(
                "INSERT INTO approvals(approval_id,task_id,action,state) VALUES(?,?,?,?)",
                (str(request.approval_id), str(request.task_id), request.action, request.state.value),
            )
            self._conn.commit()
        return request

    def create_execution(
        self,
        task_id: UUID,
        run_id: str,
        plan_id: UUID,
        invocations: tuple[ToolInvocation, ...],
        *,
        action: str,
    ) -> ApprovalExecution:
        if not run_id.strip():
            raise ValueError("run_id must not be empty")
        if not invocations:
            raise ValueError("approval execution requires at least one invocation")
        for invocation in invocations:
            invocation.validate_bounds()

        request = self._machine.request(task_id, action)
        payload = json.dumps([invocation.model_dump(mode="json") for invocation in invocations], separators=(",", ":"))
        with self._lock:
            try:
                self._conn.execute("BEGIN")
                self._conn.execute(
                    "INSERT INTO approvals(approval_id,task_id,action,state) VALUES(?,?,?,?)",
                    (str(request.approval_id), str(request.task_id), request.action, request.state.value),
                )
                self._conn.execute(
                    "INSERT INTO approval_executions(approval_id,run_id,plan_id,invocations) VALUES(?,?,?,?)",
                    (str(request.approval_id), run_id, str(plan_id), payload),
                )
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise
        return ApprovalExecution(request, run_id, plan_id, invocations)

    def get(self, approval_id: UUID) -> ApprovalRequest | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT approval_id,task_id,action,state FROM approvals WHERE approval_id=?",
                (str(approval_id),),
            ).fetchone()
        return self._request_from_row(row) if row else None

    def approve(self, approval_id: UUID) -> ApprovalRequest:
        with self._lock:
            row = self._conn.execute(
                "SELECT approval_id,task_id,action,state FROM approvals WHERE approval_id=?",
                (str(approval_id),),
            ).fetchone()
            if row is None:
                raise KeyError("approval not found")
            current = self._request_from_row(row)
            updated = self._machine.approve(current)
            cursor = self._conn.execute(
                "UPDATE approvals SET state=? WHERE approval_id=? AND state=?",
                (updated.state.value, str(approval_id), ApprovalState.PENDING.value),
            )
            if cursor.rowcount != 1:
                raise ValueError("approval state changed concurrently")
            self._conn.commit()
            return updated

    def reject(self, approval_id: UUID) -> ApprovalRequest:
        with self._lock:
            row = self._conn.execute(
                "SELECT approval_id,task_id,action,state FROM approvals WHERE approval_id=?",
                (str(approval_id),),
            ).fetchone()
            if row is None:
                raise KeyError("approval not found")
            current = self._request_from_row(row)
            updated = self._machine.reject(current)
            self._conn.execute(
                "UPDATE approvals SET state=? WHERE approval_id=? AND state=?",
                (updated.state.value, str(approval_id), ApprovalState.PENDING.value),
            )
            if self._conn.total_changes != 1:
                raise ValueError("approval state changed concurrently")
            self._conn.commit()
            return updated

    def consume_execution(self, approval_id: UUID) -> ApprovalExecution:
        """Atomically consume an approved execution; repeated resume is rejected."""
        with self._lock:
            row = self._conn.execute(
                """
                SELECT a.approval_id,a.task_id,a.action,a.state,
                       e.run_id,e.plan_id,e.invocations
                FROM approvals a
                JOIN approval_executions e ON e.approval_id=a.approval_id
                WHERE a.approval_id=?
                """,
                (str(approval_id),),
            ).fetchone()
            if row is None:
                raise KeyError("approval execution not found")

            request = self._request_from_row(row[:4])
            if request.state is not ApprovalState.APPROVED:
                raise ValueError("approval is not approved or was already consumed")

            updated = self._machine.consume(request)
            cursor = self._conn.execute(
                "UPDATE approvals SET state=? WHERE approval_id=? AND state=?",
                (updated.state.value, str(approval_id), ApprovalState.APPROVED.value),
            )
            if cursor.rowcount != 1:
                self._conn.rollback()
                raise ValueError("approval was already consumed")
            self._conn.commit()

        raw_invocations = json.loads(row[6])
        invocations = tuple(ToolInvocation.model_validate(item) for item in raw_invocations)
        for invocation in invocations:
            invocation.validate_bounds()
        return ApprovalExecution(
            updated,
            str(row[4]),
            UUID(str(row[5])),
            invocations,
        )

    def list(self) -> list[ApprovalRequest]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT approval_id,task_id,action,state FROM approvals ORDER BY rowid DESC"
            ).fetchall()
        return [self._request_from_row(row) for row in rows]

    @staticmethod
    def _request_from_row(row: tuple[object, ...]) -> ApprovalRequest:
        return ApprovalRequest(
            UUID(str(row[0])),
            UUID(str(row[1])),
            str(row[2]),
            ApprovalState(str(row[3])),
        )
