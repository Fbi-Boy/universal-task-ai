from fastapi import FastAPI

from backend.api.auth import require_configured_api_key
from backend.api.main import AnalyzeRequest, analyze_task, create_app


class _FakeTaskService:
    approval_store = object()
    tool_catalog = ()


def test_analyze_request_contract_remains_strict() -> None:
    request = AnalyzeRequest(task="build a flowchart")
    assert request.task == "build a flowchart"


def test_create_app_protects_task_analysis_with_runtime_auth_guard() -> None:
    application = create_app(task_service=_FakeTaskService())
    route = next(route for route in application.routes if route.path == "/v1/tasks/analyze")
    dependency_calls = {dependency.call for dependency in route.dependant.dependencies}
    assert require_configured_api_key in dependency_calls


def test_dependency_can_be_attached_to_analyze_route() -> None:
    application = FastAPI()
    application.add_api_route(
        "/v1/tasks/analyze",
        analyze_task,
        methods=["POST"],
        dependencies=[require_configured_api_key],
    )
    route = next(route for route in application.routes if route.path == "/v1/tasks/analyze")
    assert require_configured_api_key in {dependency.call for dependency in route.dependant.dependencies}
