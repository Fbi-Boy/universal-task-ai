from dataclasses import dataclass
from typing import Any, Mapping
from uuid import UUID

from backend.core.audit import AuditEvent, AuditEventType
from backend.core.permissions import ToolPermission, authorize_tool
from backend.core.tools import ToolRegistry, ToolResult


@dataclass(frozen=True)
class ExecutionOutcome:
    result: ToolResult
    events: tuple[AuditEvent, ...]


def execute_registered_tool(
    *,
    task_id: UUID,
    tool_name: str,
    arguments: Mapping[str, Any],
    registry: ToolRegistry,
    permissions: ToolPermission,
) -> ExecutionOutcome:
    events: list[AuditEvent] = [
        AuditEvent(event_type="task_started", task_id=task_id),
    ]
    tool = registry.get(tool_name)
    authorize_tool(tool_name=tool_name, metadata=tool.metadata, permissions=permissions)
    events.append(AuditEvent(event_type="tool_authorized", task_id=task_id, tool_name=tool_name))
    events.append(AuditEvent(event_type="tool_started", task_id=task_id, tool_name=tool_name))
    try:
        result = tool.run(arguments)
    except Exception as exc:
        events.append(AuditEvent(event_type="tool_finished", task_id=task_id, tool_name=tool_name, success=False, metadata={"error": type(exc).__name__}))
        events.append(AuditEvent(event_type="task_failed", task_id=task_id, success=False))
        raise
    events.append(AuditEvent(event_type="tool_finished", task_id=task_id, tool_name=tool_name, success=result.success))
    events.append(AuditEvent(event_type="task_finished", task_id=task_id, success=result.success))
    return ExecutionOutcome(result=result, events=tuple(events))
