from uuid import uuid4

from backend.core.audit import AuditEvent
from backend.core.audited_executor import AuditedToolExecutor
from backend.core.tools import Tool, ToolMetadata, ToolRegistry, ToolResult


class Sink:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(event)


class EchoTool(Tool):
    metadata = ToolMetadata(name="echo", description="echo")

    def run(self, arguments):
        return ToolResult(success=True, output=arguments["value"])


def test_executor_emits_start_and_finish_events() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())
    sink = Sink()
    result = AuditedToolExecutor(registry, sink, uuid4()).execute_tool("echo", {"value": "ok"})
    assert result.success
    assert [event.event_type for event in sink.events] == ["tool_started", "tool_finished"]
    assert sink.events[-1].success is True


def test_executor_records_tool_failure_result() -> None:
    class BadTool(Tool):
        metadata = ToolMetadata(name="bad", description="bad")
        def run(self, arguments):
            return ToolResult(success=False, error="failed")

    registry = ToolRegistry()
    registry.register(BadTool())
    sink = Sink()
    result = AuditedToolExecutor(registry, sink, uuid4()).execute_tool("bad", {})
    assert not result.success
    assert sink.events[-1].success is False
    assert sink.events[-1].metadata == {"has_error": True}
