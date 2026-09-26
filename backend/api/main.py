from pathlib import Path
import os

from fastapi import Depends, FastAPI, HTTPException, status
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

app = FastAPI(title="Universal Task AI", version="0.1.0")
app.include_router(approval_router, dependencies=[Depends(require_configured_api_key)])
app.include_router(runs_router, dependencies=[Depends(require_configured_api_key)])
app.include_router(events_router, dependencies=[Depends(require_configured_api_key)])
app.include_router(settings_router, dependencies=[Depends(require_configured_api_key)])


@app.get("/", include_in_schema=False)
def web_ui() -> FileResponse:
    return FileResponse("backend/web/index.html")


@app.get("/ui.js", include_in_schema=False)
def web_js() -> FileResponse:
    return FileResponse("backend/web/ui.js")


@app.get("/ui.css", include_in_schema=False)
def web_css() -> FileResponse:
    return FileResponse("backend/web/ui.css")


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    task: str = Field(min_length=1, max_length=20_000)


class AnalyzeResponse(BaseModel):
    analysis: TaskAnalysis


class TaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    task: str = Field(min_length=1, max_length=20_000)
    tool_invocations: list[ToolInvocation] = Field(default_factory=list, max_length=8)
    approval_required: bool = False


class TaskResponse(BaseModel):
    run_id: str
    status: str
    output: str
    plan_id: str
    approval_id: str | None = None


_task_store = SQLiteRunStateStore(Path(os.environ.get("UTA_RUN_STATE_DB", ".universal_task_ai_runs.sqlite3")))
_approval_store = ApprovalStore(Path(os.environ.get("UTA_APPROVAL_DB", ".universal_task_ai_approvals.sqlite3")))
_audit_sink = SQLiteAuditSink(Path(os.environ.get("UTA_AUDIT_DB", ".universal_task_ai_audit.sqlite3")))
_tool_boundary = build_runtime_tool_boundary()
_task_executor = TaskExecutor(_task_store, _tool_boundary, _audit_sink, _approval_store)
_task_service = TaskService(TaskIntakeService(), TaskPlanner(), _task_executor)
app.state.task_service = _task_service


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/tasks/analyze", response_model=AnalyzeResponse)
def analyze_task(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(analysis=TaskAnalysis.from_task_text(request.task))


@app.post("/v1/tasks", response_model=TaskResponse, dependencies=[Depends(require_configured_api_key)])
def run_task(request: TaskRequest) -> TaskResponse:
    try:
        result = _task_service.run(
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
