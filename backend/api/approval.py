from pathlib import Path
import os
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from backend.core.approval_store import ApprovalStore


class ApprovalCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    task_id: UUID
    action: str = Field(min_length=1, max_length=2_000)


class ApprovalResumeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    run_id: str = Field(min_length=1, max_length=128)
    approval_id: UUID
    actor_id: str = Field(min_length=1, max_length=128)


class ApprovalResumeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str
    status: str
    output: str
    plan_id: UUID


class ApprovalExecutionInfoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    approval_id: UUID
    task_id: UUID
    run_id: str
    plan_id: UUID
    state: str


store = ApprovalStore(Path(os.environ.get("UTA_APPROVAL_DB", ".universal_task_ai_approvals.sqlite3")))


def create_router(store: ApprovalStore) -> APIRouter:
    """Build approval routes against the exact store used by task execution."""
    router = APIRouter(prefix="/v1/approvals", tags=["approvals"])

    @router.post("")
    def create_approval(request: ApprovalCreate):
        return store.create(request.task_id, request.action)

    @router.get("")
    def list_approvals():
        return store.list()

    @router.get("/{approval_id}")
    def get_approval(approval_id: UUID):
        approval = store.get(approval_id)
        if approval is None:
            raise HTTPException(status_code=404, detail="approval not found")
        return approval

    @router.get("/{approval_id}/execution", response_model=ApprovalExecutionInfoResponse)
    def execution_info(approval_id: UUID):
        info = store.get_execution_info(approval_id)
        if info is None:
            raise HTTPException(status_code=404, detail="approval execution not found")
        return ApprovalExecutionInfoResponse(
            approval_id=info.approval_id,
            task_id=info.task_id,
            run_id=info.run_id,
            plan_id=info.plan_id,
            state=info.state.value,
        )

    @router.post("/{approval_id}/approve")
    def approve(approval_id: UUID):
        try:
            return store.approve(approval_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="approval not found")
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.post("/{approval_id}/reject")
    def reject(approval_id: UUID):
        try:
            return store.reject(approval_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="approval not found")
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.post("/{approval_id}/resume", response_model=ApprovalResumeResponse)
    def resume(approval_id: UUID, request: ApprovalResumeRequest, http_request: Request):
        if request.approval_id != approval_id:
            raise HTTPException(status_code=400, detail="approval_id does not match path")
        service = getattr(http_request.app.state, "task_service", None)
        if service is None:
            raise HTTPException(status_code=503, detail="task service is not configured")
        try:
            result = service.resume_approved(
                run_id=request.run_id,
                approval_id=str(approval_id),
                actor_id=request.actor_id,
            )
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return ApprovalResumeResponse(
            run_id=result.run_id,
            status=result.status.value,
            output=result.output,
            plan_id=result.plan.plan_id,
        )

    return router


router = create_router(
    ApprovalStore(Path(os.environ.get("UTA_APPROVAL_DB", ".universal_task_ai_approvals.sqlite3")))
)


# Backward-compatible direct handlers for existing internal callers/tests.
_default_router_store = store


def create_approval(request: ApprovalCreate):
    return _default_router_store.create(request.task_id, request.action)


def list_approvals():
    return _default_router_store.list()


def get_approval(approval_id: UUID):
    approval = _default_router_store.get(approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="approval not found")
    return approval


def approve(approval_id: UUID):
    try:
        return _default_router_store.approve(approval_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="approval not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


def reject(approval_id: UUID):
    try:
        return _default_router_store.reject(approval_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="approval not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
