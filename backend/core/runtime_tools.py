from pathlib import Path

from backend.core.audit_sink import SQLiteAuditSink
from backend.core.permissions import ToolPermission
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tools import ToolRegistry
from backend.tools.calculator import CalculatorTool


def build_runtime_tool_boundary() -> RuntimeToolBoundary:
    """Build the default least-privilege runtime tool set."""
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    return RuntimeToolBoundary(
        registry,
        ToolPermission(frozenset({"calculator"})),
    )


def build_audit_sink(path: Path) -> SQLiteAuditSink:
    return SQLiteAuditSink(path)
