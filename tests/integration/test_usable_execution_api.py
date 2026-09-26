from pathlib import Path
from uuid import uuid4

from backend.api.approval import create_router
from backend.core.approval_store import ApprovalStore
from backend.core.runtime_tools import build_runtime_tool_boundary
from backend.core.tool_invocation import ToolInvocation
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(
        name="echo",
        description="test echo",
        risk_level="low",
    )

    def run(self, arguments):
        return ToolResult(success=True, output=arguments.get("value", ""))


def _endpoint(router, path: str):
    return next(route.endpoint for route in router.routes if getattr(route, "path", None) == path)


def test_default_runtime_catalog_is_least_privilege(monkeypatch):
    monkeypatch.delenv("UTA_LOCAL_ROOTS", raising=False)
    monkeypatch.delenv("UTA_BROWSER_ENABLED", raising=False)
    monkeypatch.delenv("UTA_PYTHON_SANDBOX_ENABLED", raising=False)

    catalog = build_runtime_tool_boundary().catalog()

    assert [item.name for item in catalog] == ["calculator"]
    assert catalog[0].requires_network is False
    assert catalog[0].requires_approval is False


def test_approval_execution_metadata_never_exposes_invocation_arguments(tmp_path: Path):
    store = ApprovalStore(tmp_path / "approvals.sqlite3")
    invocation = ToolInvocation(tool_name="echo", arguments={"value": "safe"})
    request = store.create_execution(
        uuid4(),
        "run-usable-ui",
        uuid4(),
        (invocation,),
        action="execute echo",
    )

    router = create_router(store)
    endpoint = _endpoint(router, "/v1/approvals/{approval_id}/execution")
    info = endpoint(request.request.approval_id)

    assert info.run_id == "run-usable-ui"
    assert info.approval_id == request.request.approval_id
    assert not hasattr(info, "invocations")


def test_approval_execution_metadata_404s_for_plain_approval():
    store = ApprovalStore()
    approval_id = uuid4()
    # The UUID is deliberately absent; the endpoint must not manufacture
    # execution state for an unrelated approval identifier.
    router = create_router(store)
    endpoint = _endpoint(router, "/v1/approvals/{approval_id}/execution")
    try:
        endpoint(approval_id)
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 404
    else:
        raise AssertionError("missing execution metadata must return 404")
