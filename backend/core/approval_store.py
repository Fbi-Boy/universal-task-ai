import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
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
    contract_hash: str = ""
    plan_hash: str = ""


@dataclass(frozen=True)
class ApprovalExecutionInfo:
    approval_id: UUID
    task_id: UUID
    run_id: str
    plan_id: UUID
    state: ApprovalState
    decided_by: str | None = None
    decided_at: str | None = None


class ApprovalStore:
    """SQLite-backed approval store with atomic approval consumption.

    The default in-memory database preserves isolated unit-test behavior.
    Production callers should provide a persistent path.
    """

    def __init__(self, path: Path | str = ":memory:", machine: ApprovalMachine | None = None) -> None:
        self._machine = machine or ApprovalMachine()
        self._lock = Lock()
        self._conn = sqlite3.connect(str(path), check_same_thread=False)
        self._conn.execute("PRAGMA foreign_keys=ON")
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
                contract_hash TEXT,
                plan_hash TEXT,
                FOREIGN KEY(approval_id) REFERENCES approvals(approval_id)
            )
            """
        )
        self._ensure_decision_columns()
        self._ensure_execution_integrity_columns()
        self._conn.commit()

    def _ensure_decision_columns(self) -> None:
        columns = {str(row[1]) for row in self._conn.execute("PRAGMA table_info(approvals)").fetchall()}
        if "decided_by" not in columns:
            self._conn.execute("ALTER TABLE approvals ADD COLUMN decided_by TEXT")
        if "decided_at" not in columns:
            self._conn.execute("ALTER TABLE approvals ADD COLUMN decided_at TEXT")

    def _ensure_execution_integrity_columns(self) -> None:
        columns = {str(row[1]) for row in self._conn.execute("PRAGMA table_info(approval_executions)").fetchall()}
        if "contract_hash" not in columns:
            self._conn.execute("ALTER TABLE approval_executions ADD COLUMN contract_hash TEXT")
        if "plan_hash" not in columns:
            self._conn.execute("ALTER TABLE approval_executions ADD COLUMN plan_hash TEXT")

    @staticmethod
    def _validate_actor(actor_id: str) -> str:
        actor = actor_id.strip()
        if not actor:
            raise ValueError("actor_id must not be empty")
        if len(actor) > 128:
            raise ValueError("actor_id must be at most 128 characters")
        return actor

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
        contract_hash: str = "",
        plan_hash: str = "",
    ) -> ApprovalExecution:
        if not run_id.strip():
            raise ValueError("run_id must not be empty")
        if len(run_id) > 128:
            raise ValueError("run_id must be at most 128 characters")
        if not invocations:
            raise ValueError("approval execution requires at least one invocation")
        if contract_hash or plan_hash:
            if len(contract_hash) != 64 or len(plan_hash) != 64:
                raise ValueError("execution manifest hashes must be SHA-256 hex digests")
            if any(char not in "0123456789abcdef" for char in contract_hash + plan_hash):
                raise ValueError("execution manifest hashes must be lowercase hexadecimal")
        if len(invocations) > 8:
            raise ValueError("approval execution supports at most 8 invocations")
        if len(action.strip()) > 2_000:
            raise ValueError("approval action must be at most 2000 characters")
        for invocation in invocations:
            invocation.validate_bounds()
            self._reject_secret_arguments(invocation.arguments)

        request = self._machine.request(task_id, action)
        payload = json.dumps(
            [invocation.model_dump(mode="json") for invocation in invocations],
            separators=(",", ":"),
        )
        if len(payload.encode("utf-8")) > 256 * 1024:
            raise ValueError("approval execution manifest exceeds 256 KiB")
        with self._lock:
            try:
                self._conn.execute("BEGIN")
                self._conn.execute(
                    "INSERT INTO approvals(approval_id,task_id,action,state) VALUES(?,?,?,?)",
                    (str(request.approval_id), str(request.task_id), request.action, request.state.value),
                )
                self._conn.execute(
                    "INSERT INTO approval_executions(approval_id,run_id,plan_id,invocations,contract_hash,plan_hash) VALUES(?,?,?,?,?,?)",
                    (str(request.approval_id), run_id, str(plan_id), payload, contract_hash, plan_hash),
                )
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise
        return ApprovalExecution(request, run_id, plan_id, invocations, contract_hash, plan_hash)

    def get(self, approval_id: UUID) -> ApprovalRequest | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT approval_id,task_id,action,state FROM approvals WHERE approval_id=?",
                (str(approval_id),),
            ).fetchone()
        return self._request_from_row(row) if row else None

    def get_execution_info(self, approval_id: UUID) -> ApprovalExecutionInfo | None:
        """Return non-secret resume metadata without exposing invocation arguments."""
        with self._lock:
            row = self._conn.execute(
                """
                SELECT a.approval_id,a.task_id,a.state,e.run_id,e.plan_id,a.decided_by,a.decided_at
                FROM approvals a
                JOIN approval_executions e ON e.approval_id=a.approval_id
                WHERE a.approval_id=?
                """,
                (str(approval_id),),
            ).fetchone()
        if row is None:
            return None
        return ApprovalExecutionInfo(
            approval_id=UUID(str(row[0])),
            task_id=UUID(str(row[1])),
            run_id=str(row[3]),
            plan_id=UUID(str(row[4])),
            state=ApprovalState(str(row[2])),
            decided_by=str(row[5]) if row[5] is not None else None,
            decided_at=str(row[6]) if row[6] is not None else None,
        )

    def approve(self, approval_id: UUID, actor_id: str) -> ApprovalRequest:
        return self._decide(approval_id, actor_id, approved=True)

    def reject(self, approval_id: UUID, actor_id: str) -> ApprovalRequest:
        return self._decide(approval_id, actor_id, approved=False)

    def _decide(self, approval_id: UUID, actor_id: str, *, approved: bool) -> ApprovalRequest:
        actor = self._validate_actor(actor_id)
        with self._lock:
            row = self._conn.execute(
                "SELECT approval_id,task_id,action,state FROM approvals WHERE approval_id=?",
                (str(approval_id),),
            ).fetchone()
            if row is None:
                raise KeyError("approval not found")
            current = self._request_from_row(row)
            updated = self._machine.approve(current) if approved else self._machine.reject(current)
            decided_at = datetime.now(timezone.utc).isoformat()
            cursor = self._conn.execute(
                "UPDATE approvals SET state=?, decided_by=?, decided_at=? WHERE approval_id=? AND state=?",
                (updated.state.value, actor, decided_at, str(approval_id), ApprovalState.PENDING.value),
            )
            if cursor.rowcount != 1:
                self._conn.rollback()
                raise ValueError("approval state changed concurrently")
            self._conn.commit()
            return updated
    def consume_execution(self, approval_id: UUID, *, expected_contract_hash: str | None = None, expected_plan_hash: str | None = None) -> ApprovalExecution:
        """Atomically consume an approved execution after manifest integrity checks."""
        with self._lock:
            row = self._conn.execute(
                """
                SELECT a.approval_id,a.task_id,a.action,a.state,
                       e.run_id,e.plan_id,e.invocations,e.contract_hash,e.plan_hash
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
            if expected_contract_hash is not None and str(row[7] or "") != expected_contract_hash:
                raise ValueError("approval execution contract manifest has changed")
            if expected_plan_hash is not None and str(row[8] or "") != expected_plan_hash:
                raise ValueError("approval execution plan manifest has changed")

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
        return ApprovalExecution(updated, str(row[4]), UUID(str(row[5])), invocations, str(row[7] or ""), str(row[8] or ""))

    def list(self) -> list[ApprovalRequest]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT approval_id,task_id,action,state FROM approvals ORDER BY rowid DESC"
            ).fetchall()
        return [self._request_from_row(row) for row in rows]

    @staticmethod
    def _reject_secret_arguments(arguments: object) -> None:
        blocked = {"password", "token", "secret", "api_key", "authorization", "cookie"}

        def walk(value: object, depth: int = 0) -> None:
            if depth > 8:
                raise ValueError("approval execution arguments exceed maximum nesting depth")
            if isinstance(value, dict):
                for key, item in value.items():
                    if str(key).lower() in blocked:
                        raise ValueError("approval execution arguments must not contain secret-bearing fields")
                    walk(item, depth + 1)
            elif isinstance(value, (list, tuple)):
                for item in value:
                    walk(item, depth + 1)

        walk(arguments)

    @staticmethod
    def _request_from_row(row: tuple[object, ...]) -> ApprovalRequest:
        return ApprovalRequest(
            UUID(str(row[0])),
            UUID(str(row[1])),
            str(row[2]),
            ApprovalState(str(row[3])),
        )

    def ping(self) -> None:
        """Verify that the durable approval database is responsive."""
        with self._lock:
            self._conn.execute("SELECT 1").fetchone()
