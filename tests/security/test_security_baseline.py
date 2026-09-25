from pathlib import Path
from uuid import uuid4

from backend.core.audit import AuditEvent
from backend.core.permissions import ToolPermission, PermissionDenied
from backend.core.schemas import TaskContract
from backend.core.secrets import redact_metadata
from backend.tools.file_reader import FileReaderTool


def test_secret_redaction() -> None:
    result = redact_metadata({"token": "hidden", "name": "ok"})
    assert result["token"] == "[REDACTED]"
    assert result["name"] == "ok"


def test_high_risk_contract_requires_approval() -> None:
    from backend.core.validation import validate_task_contract
    task = TaskContract(goal="danger", risk_level="high")
    assert not validate_task_contract(task).passed


def test_permission_denies_unlisted_tool() -> None:
    try:
        from backend.core.permissions import authorize_tool
        from backend.core.tools import ToolMetadata
        authorize_tool(ToolMetadata(name="missing", description=""), ToolPermission(frozenset()))
    except PermissionDenied:
        return
    raise AssertionError("permission check did not fail closed")


def test_audit_filters_secret_keys() -> None:
    event = AuditEvent(event_type="task_started", task_id=uuid4(), metadata={"api_key": "x", "safe": "y"})
    assert "api_key" not in event.safe_metadata()
    assert event.safe_metadata()["safe"] == "y"


def test_file_reader_cannot_escape_root(tmp_path: Path) -> None:
    outside = tmp_path.parent / "sensitive.txt"
    outside.write_text("secret", encoding="utf-8")
    result = FileReaderTool(tmp_path).run({"path": "../sensitive.txt"})
    assert not result.success
