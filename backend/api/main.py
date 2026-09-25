from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from backend.core.analyzer import TaskAnalysis
from backend.api.approval import router as approval_router
from backend.api.runs import router as runs_router
from backend.api.events import router as events_router
from backend.api.settings import router as settings_router

app = FastAPI(title="Universal Task AI", version="0.1.0")
app.include_router(approval_router)
app.include_router(runs_router)
app.include_router(events_router)
app.include_router(settings_router)


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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/tasks/analyze", response_model=AnalyzeResponse)
def analyze_task(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(analysis=TaskAnalysis.from_task_text(request.task))
