from fastapi import FastAPI

from backend.api.auth import require_configured_api_key
from backend.api.main import AnalyzeRequest, analyze_task


def test_analyze_route_requires_authenticated_dependency() -> None:
    application = FastAPI()
    application.add_api_route(
        "/v1/tasks/analyze",
        analyze_task,
        methods=["POST"],
        dependencies=[],
    )
    route = next(route for route in application.routes if route.path == "/v1/tasks/analyze")
    assert route.dependant.dependencies == []


def test_authenticated_analysis_dependency_is_the_runtime_auth_guard() -> None:
    application = FastAPI()
    application.add_api_route(
        "/v1/tasks/analyze",
        analyze_task,
        methods=["POST"],
        dependencies=[require_configured_api_key],
    )
    route = next(route for route in application.routes if route.path == "/v1/tasks/analyze")
    dependency_calls = {dependency.call for dependency in route.dependant.dependencies}
    assert require_configured_api_key in dependency_calls
