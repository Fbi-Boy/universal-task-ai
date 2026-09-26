from pathlib import Path
import os

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from backend.api.approval import router as approval_router
from backend.api.auth import require_configured_api_key
from backend.api.events import router as events_router
from backend.api.runs import router as runs_router
from backend.api.settings import router as settings_router
from backend.core.analyzer import TaskAnalysis
from backend.core.approval_store import ApprovalStore
from backend.core.audit_sink import SQLiteAuditSink
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner
from backend.core.task_service import TaskService
from backend.core.tool_invocation import ToolInvocation
from backend.core.runtime_tools import build_runtime_tool_boundary

def build_task_service(
    run_state_path: Path,
    approval_path: Path,
    audit_path: Path,
) -> TaskService:
    return TaskService(
        TaskIntakeService(),
        TaskPlanner(),
        TaskExecutor(
            SQLiteRunStateStore(run_state_path),
            build_runtime_tool_boundary(),
            SQLiteAuditSink(audit_path),
            ApprovalStore(approval_path),
        ),
    )


def create_app(*, task_service: TaskService | None = None) -> FastAPI:
    application = FastAPI(title="Universal Task AI", version="0.1.0")
    application.include_router(
        approval_router,
        dependencies=[Depends(require_configured_api_key)],
    )
    application.include_router(
        runs_router,
        dependencies=[Depends(require_configured_api_key)],
    )
    application.include_router(
        events_router,
        dependencies=[Depends(require_configured_api_key)],
    )
    application.include_router(
        settings_router,
        dependencies=[Depends(require_configured_api_key)],
    )

    @application.get("/", include_in_schema=False)
    def web_ui() -> FileResponse:
        return FileResponse("backend/web/index.html")

    @application.get("/ui.js", include_in_schema=False)
    def web_js() -> FileResponse:
        return FileResponse("backend/web/ui.js")

    @application.get("/ui.css", include_in_schema=False)
    def web_css() -> FileResponse:
        return FileResponse("backend/web/ui.css")

    application.state.task_service = task_service or build_task_service(
        Path(os.environ.get("UTA_RUN_STATE_DB", ".universal_task_ai_runs.sqlite3")),
        Path(os.environ.get("UTA_APPROVAL_DB", ".universal_task_ai_approvals.sqlite3")),
        Path(os.environ.get("UTA_AUDIT_DB", ".universal_task_ai_audit.sqlite3")),
    )
    return application


app = create_app()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/tasks/analyze", response_model=AnalyzeResponse)
def analyze_task(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(analysis=TaskAnalysis.from_task_text(request.task))


@app.post("/v1/tasks", response_model=TaskResponse, dependencies=[Depends(require_configured_api_key)])
def run_task(request: TaskRequest, http_request: Request) -> TaskResponse:
    try:
        result = http_request.app.state.task_service.run(
            request.task,
            tool_invocations=tuple(request.tool_invocations),
            approval_required=request.approval_required,
        )
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return TaskResponse(
        run_id=result.execution.run_id,
        status=result.execution.status.value,
        output=result.execution.output,
        plan_id=str(result.execution.plan.plan_id),
        approval_id=result.execution.approval_id,
    )
