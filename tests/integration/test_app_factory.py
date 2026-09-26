from pathlib import Path

from backend.api.main import build_task_service, create_app
from backend.core.approval_store import ApprovalStore
from backend.core.tool_invocation import ToolInvocation


class StubTaskService:
    approval_store = ApprovalStore()

    def run(self, task_text: str, **kwargs):
        raise AssertionError("stub should not be called by app construction")


def test_create_app_accepts_injected_task_service():
    service = StubTaskService()
    app = create_app(task_service=service)
    assert app.state.task_service is service


def test_build_task_service_uses_persistent_runtime_paths(tmp_path: Path):
    service = build_task_service(
        tmp_path / "runs.sqlite3",
        tmp_path / "approvals.sqlite3",
        tmp_path / "audit.sqlite3",
    )

    result = service.run(
        "calculate",
        tool_invocations=(
            ToolInvocation(tool_name="calculator", arguments={"expression": "7 * 6"}),
        ),
    )

    assert result.execution.status.value == "succeeded"
    assert result.execution.output == "42"
    assert (tmp_path / "audit.sqlite3").exists()
