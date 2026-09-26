from pathlib import Path
from uuid import UUID

from backend.api.main import build_task_service, create_app
from backend.core.approval_store import ApprovalStore
from backend.core.tool_invocation import ToolInvocation


def _endpoint(app, path: str):
    return next(route.endpoint for route in app.routes if getattr(route, "path", None) == path)


def test_approval_api_uses_the_same_store_as_task_executor(tmp_path: Path):
    service = build_task_service(
        tmp_path / "runs.sqlite3",
        tmp_path / "approvals.sqlite3",
        tmp_path / "audit.sqlite3",
    )
    app = create_app(task_service=service)

    assert service.approval_store is not None

    waiting = service.run(
        "calculate after approval",
        tool_invocations=(
            ToolInvocation(tool_name="calculator", arguments={"expression": "8 * 7"}),
        ),
        approval_required=True,
    )

    assert waiting.execution.status.value == "waiting_approval"
    approval_id = UUID(waiting.execution.approval_id)

    approve_endpoint = _endpoint(app, "/v1/approvals/{approval_id}/approve")
    approved = approve_endpoint(approval_id)

    assert approved.approval_id == approval_id
    assert approved.state.value == "approved"
    assert service.approval_store.get(approval_id).state.value == "approved"


def test_task_service_exposes_executor_approval_store(tmp_path: Path):
    service = build_task_service(
        tmp_path / "runs.sqlite3",
        tmp_path / "approvals.sqlite3",
        tmp_path / "audit.sqlite3",
    )

    assert isinstance(service.approval_store, ApprovalStore)
