from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from backend.core.analyzer import TaskAnalysis
from backend.api.approval import router as approval_router

app = FastAPI(title="Universal Task AI", version="0.1.0")
app.include_router(approval_router)


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
