from uuid import UUID
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from backend.core.approval import ApprovalState
from backend.core.approval_store import ApprovalStore

router = APIRouter(prefix="/v1/approvals", tags=["approvals"])
store = ApprovalStore(Path(os.environ.get("UTA_APPROVAL_DB", ".universal_task_ai_approvals.sqlite3")) )


class ApprovalCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    task_id: UUID
    action: str = Field(min_length=1, max_length=2_000)


@router.post("")
def create_approval(request: ApprovalCreate):
    return store.create(request.task_id, request.action)


@router.get("")
def list_approvals():
    return store.list()


@router.get("/{approval_id}")
def get_approval(approval_id: UUID):
    request = store.get(approval_id)
    if request is None:
        raise HTTPException(status_code=404, detail="approval not found")
    return request


@router.post("/{approval_id}/approve")
def approve(approval_id: UUID):
    try:
        return store.approve(approval_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="approval not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.post("/{approval_id}/reject")
def reject(approval_id: UUID):
    try:
        return store.reject(approval_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="approval not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
