from uuid import uuid4

from backend.core.execution import execute_registered_tool
from backend.core.permissions import ToolPermission
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class EchoTool(Tool):
    metadata = ToolMetadata(name="echo", description="test")


    def run(self, arguments: dict[str, object]) -> ToolResult:
        return ToolResult(success=True, output=arguments)


def test_execution_emits_audit_lifecycle() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())
    outcome = execute_registered_tool(
        task_id=uuid4(),
        tool_name="echo",
        arguments={"x": 1},
        registry=registry,
        permissions=ToolPermission(frozenset({"echo"})),
    )
    assert outcome.result.output == {"x": 1}
    assert [e.event_type for e in outcome.events] == [
        "task_started", "tool_authorized", "tool_started", "tool_finished", "task_finished"
    ]
