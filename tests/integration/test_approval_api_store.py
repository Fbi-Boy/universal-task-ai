from pathlib import Path
from uuid import UUID

from starlette.requests import Request

from backend.api.main import build_task_service, create_app
from backend.core.tool_invocation import ToolInvocation


def _request_for_app(app) -> Request:
    return Request({"type": "http", "method": "POST", "path": "/", "headers": [], "app": app})


def _endpoint(app, path: str):
    return next(route.endpoint for route in app.routes if getattr(route, "path", None) == path)


def test_approval_api_uses_the_same_store_as_task_executor(tmp_path: Path):
    service = build_task_service(
        tmp_path / "runs.sqlite3",
        tmp_path / "approvals.sqlite3",
        tmp_path / "audit.sqlite3",
    )
    app = create_app(task_service=service)

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


def test_approval_api_resume_consumes_the_same_execution_store(tmp_path: Path):
    service = build_task_service(
        tmp_path / "runs.sqlite3",
        tmp_path / "approvals.sqlite3",
        tmp_path / "audit.sqlite3",
    )
    app = create_app(task_service=service)

    waiting = service.run(
        "calculate after approval",
        tool_invocations=(
            ToolInvocation(tool_name="calculator", arguments={"expression": "8 * 7"}),
        ),
        approval_required=True,
    )
    approval_id = UUID(waiting.execution.approval_id)

    approve_endpoint = _endpoint(app, "/v1/approvals/{approval_id}/approve")
    approve_endpoint(approval_id)

    resume_endpoint = _endpoint(app, "/v1/approvals/{approval_id}/resume")
    response = resume_endpoint(
        approval_id,
        type("Payload", (), {
            "approval_id": approval_id,
            "run_id": waiting.execution.run_id,
            "actor_id": "integration-test",
        })(),
        _request_for_app(app),
    )

    assert response.status.value == "succeeded"
    assert response.output == "56"
    assert service.approval_store.get(approval_id).state.value == "consumed"
