from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from backend.api.main import TaskRequest, _run_task_endpoint


class _DeniedTaskService:
    def run(self, *_args, **_kwargs):
        raise PermissionError("internal capability policy detail")


def _request_context():
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(task_service=_DeniedTaskService())))


def test_tool_policy_denial_returns_forbidden_without_internal_details():
    with pytest.raises(HTTPException) as caught:
        _run_task_endpoint(TaskRequest(task="read a local file"), _request_context())

    assert caught.value.status_code == 403
    assert caught.value.detail == "tool execution denied by runtime policy"
    assert "internal capability policy detail" not in str(caught.value.detail)
