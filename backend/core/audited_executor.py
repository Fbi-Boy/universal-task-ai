from typing import Any, Mapping, Protocol
from uuid import UUID

from backend.core.audit import AuditEvent
from backend.core.tools import ToolRegistry, ToolResult
from backend.core.events import ExecutionEventBus


class AuditSink(Protocol):
    def append(self, event: AuditEvent) -> None:
        ...


class AuditedToolExecutor:
    """Execute registered tools while emitting start/finish audit events."""

    def __init__(self, registry: ToolRegistry, sink: AuditSink, task_id: UUID, event_bus: ExecutionEventBus | None = None) -> None:
        self._registry = registry
        self._sink = sink
        self._task_id = task_id
        self._event_bus = event_bus

    def execute_tool(self, name: str, arguments: Mapping[str, Any]) -> ToolResult:
        if self._event_bus:
            self._event_bus.publish(self._task_id, "tool_started", name)
        self._sink.append(AuditEvent(event_type="tool_started", task_id=self._task_id, tool_name=name))
        try:
            result = self._registry.get(name).run(arguments)
        except Exception as exc:
            if self._event_bus:
                self._event_bus.publish(self._task_id, "tool_failed", name)
            self._sink.append(AuditEvent(event_type="tool_finished", task_id=self._task_id, tool_name=name, success=False, metadata={"error_type": type(exc).__name__}))
            raise
        if self._event_bus:
            self._event_bus.publish(self._task_id, "tool_finished", name)
        self._sink.append(AuditEvent(event_type="tool_finished", task_id=self._task_id, tool_name=name, success=result.success, metadata={"has_error": result.error is not None}))
        return result
