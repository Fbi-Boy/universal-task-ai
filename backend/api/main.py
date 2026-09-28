from pathlib import Path
import os

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from backend.api.approval import create_router as create_approval_router
from backend.api.auth import require_configured_api_key
from backend.api.events import router as events_router
from backend.api.hardening import SecurityHeadersMiddleware, RequestBodyLimitMiddleware, RequestContextMiddleware, request_id_from_request
from backend.api.runs import router as runs_router
from backend.api.settings import router as settings_router
from backend.core.analyzer import TaskAnalysis
from backend.core.model_task_analyzer import ModelTaskAnalyzer
from backend.core.ollama_gateway import OllamaModelGateway
from backend.core.openai_gateway import OpenAIModelGateway
from backend.core.release import build_sha, build_version
from backend.core.secret_provider import SecretProvider
from backend.core.approval_store import ApprovalStore
from backend.core.audit_sink import SQLiteAuditSink
from backend.core.runtime_tools import build_runtime_tool_boundary
from backend.core.state_store import SQLiteRunStateStore
from backend.core.task_executor import TaskExecutor
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner
from backend.core.task_service import TaskService
from backend.core.tool_invocation import ToolInvocation


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
    auto_route_tools: bool = True


class TaskResponse(BaseModel):
    run_id: str
    status: str
    output: str
    plan_id: str
    approval_id: str | None = None
    routing_mode: str
    routed_tools: list[str] = Field(default_factory=list)


class ToolCatalogItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str
    risk_level: str
    requires_network: bool
    requires_approval: bool


def build_task_service(
    run_state_path: Path,
    approval_path: Path,
    audit_path: Path,
) -> TaskService:
    approval_store = ApprovalStore(approval_path)
    intake = TaskIntakeService()
    if os.environ.get("UTA_MODEL_ENABLED", "").lower() == "true":
        model_name = os.environ.get("UTA_MODEL", "").strip()
        if not model_name:
            raise ValueError("UTA_MODEL is required when model assistance is enabled")
        provider = os.environ.get("UTA_MODEL_PROVIDER", "openai").strip().lower()
        if provider == "ollama":
            gateway = OllamaModelGateway(
                model=model_name,
                base_url=os.environ.get(
                    "UTA_OLLAMA_BASE_URL", "http://127.0.0.1:11434"
                ),
            )
        elif provider == "openai":
            gateway = OpenAIModelGateway(SecretProvider(), model=model_name)
        else:
            raise ValueError("UTA_MODEL_PROVIDER must be openai or ollama")
        intake = TaskIntakeService(ModelTaskAnalyzer(gateway))
    return TaskService(
        intake,
        TaskPlanner(),
        TaskExecutor(
            SQLiteRunStateStore(run_state_path),
            build_runtime_tool_boundary(),
            SQLiteAuditSink(audit_path),
            approval_store,
        ),
    )


def web_ui() -> FileResponse:
    return FileResponse("backend/web/index.html")


def web_js() -> FileResponse:
    return FileResponse("backend/web/ui.js")


def web_css() -> FileResponse:
    return FileResponse("backend/web/ui.css")


def health() -> dict[str, str]:
    return {"status": "ok", "version": build_version(), "build_sha": build_sha()}


def readiness(http_request: Request) -> dict[str, str]:
    service = getattr(http_request.app.state, "task_service", None)
    if service is None:
        raise HTTPException(status_code=503, detail="runtime is not ready")
    try:
        checks = service.readiness()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="runtime dependencies are not ready") from exc
    return {"status": "ready", "version": build_version(), "build_sha": build_sha(), **checks}


def list_tools(http_request: Request) -> list[ToolCatalogItem]:
    service = http_request.app.state.task_service
    return [ToolCatalogItem(**metadata.__dict__) for metadata in service.tool_catalog]


def analyze_task(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(analysis=TaskAnalysis.from_task_text(request.task))


def _run_task_endpoint(request: TaskRequest, http_request: Request) -> TaskResponse:
    service = http_request.app.state.task_service
    try:
        result = service.run(
            request.task,
            tool_invocations=tuple(request.tool_invocations),
            approval_required=request.approval_required,
            auto_route_tools=request.auto_route_tools,
        )
    except PermissionError as exc:
        # Policy details may contain internal capability names; do not expose them.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="tool execution denied by runtime policy",
        ) from exc
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return TaskResponse(
        run_id=result.execution.run_id,
        status=result.execution.status.value,
        output=result.execution.output,
        plan_id=str(result.execution.plan.plan_id),
        approval_id=result.execution.approval_id,
        routing_mode=result.routing_mode,
        routed_tools=list(result.routed_tools),
    )


def run_task(request: TaskRequest) -> TaskResponse:
    try:
        result = app.state.task_service.run(
            request.task,
            tool_invocations=tuple(request.tool_invocations),
            approval_required=request.approval_required,
            auto_route_tools=request.auto_route_tools,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="tool execution denied by runtime policy",
        ) from exc
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return TaskResponse(
        run_id=result.execution.run_id,
        status=result.execution.status.value,
        output=result.execution.output,
        plan_id=str(result.execution.plan.plan_id),
        approval_id=result.execution.approval_id,
        routing_mode=result.routing_mode,
        routed_tools=list(result.routed_tools),
    )


def create_app(*, task_service: TaskService | None = None) -> FastAPI:
    application = FastAPI(title="Universal Task AI", version=build_version())
    application.add_middleware(RequestBodyLimitMiddleware)
    application.add_middleware(SecurityHeadersMiddleware)
    application.add_middleware(RequestContextMiddleware)

    @application.exception_handler(Exception)
    async def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            {"detail": "internal server error", "request_id": request_id_from_request(request)},
            status_code=500,
            headers={"cache-control": "no-store"},
        )

    service = task_service or build_task_service(
        Path(os.environ.get("UTA_RUN_STATE_DB", ".universal_task_ai_runs.sqlite3")),
        Path(os.environ.get("UTA_APPROVAL_DB", ".universal_task_ai_approvals.sqlite3")),
        Path(os.environ.get("UTA_AUDIT_DB", ".universal_task_ai_audit.sqlite3")),
    )
    approval_store = service.approval_store
    if approval_store is None:
        raise ValueError("task service must expose its approval store")

    application.include_router(
        create_approval_router(approval_store),
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
    application.add_api_route("/", web_ui, include_in_schema=False)
    application.add_api_route("/ui.js", web_js, include_in_schema=False)
    application.add_api_route("/ui.css", web_css, include_in_schema=False)
    application.add_api_route("/health", health)
    application.add_api_route("/ready", readiness)
    application.add_api_route(
        "/v1/tools",
        list_tools,
        methods=["GET"],
        response_model=list[ToolCatalogItem],
        dependencies=[Depends(require_configured_api_key)],
    )
    application.add_api_route(
        "/v1/tasks/analyze",
        analyze_task,
        methods=["POST"],
        response_model=AnalyzeResponse,
        dependencies=[Depends(require_configured_api_key)],
    )
    application.add_api_route(
        "/v1/tasks",
        _run_task_endpoint,
        methods=["POST"],
        response_model=TaskResponse,
        dependencies=[Depends(require_configured_api_key)],
    )
    application.state.task_service = service
    return application


app = create_app()
