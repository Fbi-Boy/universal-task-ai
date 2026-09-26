import os
from pathlib import Path

from backend.core.audit_sink import SQLiteAuditSink
from backend.core.browser_policy import BrowserPolicy
from backend.core.permissions import ToolPermission
from backend.core.project_context import ProjectContextReader
from backend.core.workspace_policy import WorkspacePolicy
from backend.core.sandbox import DockerSandbox, SandboxConfig
from backend.core.tool_boundary import RuntimeToolBoundary
from backend.core.tools import ToolRegistry
from backend.local_agent.broker import LocalCapabilityBroker, LocalCapabilityPolicy
from backend.tools.browser_worker import BrowserWorkerTool
from backend.tools.calculator import CalculatorTool
from backend.tools.local_filesystem import LocalFilesystemReadTool
from backend.tools.playwright_worker import PlaywrightBrowserWorker
from backend.tools.python_sandbox import PythonSandboxTool
from backend.tools.project_context import ProjectContextTool


def _local_roots() -> tuple[Path, ...]:
    raw = os.environ.get("UTA_LOCAL_ROOTS", "")
    return tuple(Path(item).expanduser() for item in raw.split(os.pathsep) if item.strip())


def build_runtime_tool_boundary() -> RuntimeToolBoundary:
    """Build the default least-privilege runtime tool set."""
    registry = ToolRegistry()
    allowed = {"calculator"}
    allow_filesystem = False
    allow_network = False

    registry.register(CalculatorTool())

    sandbox_enabled = os.environ.get("UTA_PYTHON_SANDBOX_ENABLED", "").lower() == "true"
    if sandbox_enabled:
        image = os.environ.get("UTA_SANDBOX_IMAGE", "").strip()
        if not image:
            raise ValueError("UTA_SANDBOX_IMAGE is required when Python sandbox is enabled")
        registry.register(PythonSandboxTool(DockerSandbox(SandboxConfig(image))))
        allowed.add("python_sandbox")

    roots = _local_roots()
    if roots:
        broker = LocalCapabilityBroker(LocalCapabilityPolicy(roots))
        registry.register(LocalFilesystemReadTool(broker))
        registry.register(ProjectContextTool(ProjectContextReader(WorkspacePolicy(roots))))
        allowed.update({"filesystem.read_text", "filesystem.project_context"})
        allow_filesystem = True

    browser_enabled = os.environ.get("UTA_BROWSER_ENABLED", "").lower() == "true"
    raw_hosts = os.environ.get("UTA_BROWSER_ALLOWED_HOSTS", "")
    hosts = frozenset(item.strip().lower().rstrip(".") for item in raw_hosts.split(",") if item.strip())
    if browser_enabled:
        if not hosts:
            raise ValueError("UTA_BROWSER_ALLOWED_HOSTS is required when browser capability is enabled")
        policy = BrowserPolicy(hosts)
        registry.register(BrowserWorkerTool(policy, PlaywrightBrowserWorker(policy)))
        allowed.add("browser_worker")
        allow_network = True

    return RuntimeToolBoundary(
        registry,
        ToolPermission(
            frozenset(allowed),
            allow_network=allow_network,
            allow_filesystem=allow_filesystem,
        ),
    )


def build_audit_sink(path: Path) -> SQLiteAuditSink:
    return SQLiteAuditSink(path)
