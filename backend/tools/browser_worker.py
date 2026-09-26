from dataclasses import dataclass
from typing import Protocol

from backend.core.browser_policy import BrowserAction, BrowserPolicy
from backend.core.tools import Tool, ToolMetadata, ToolResult


@dataclass(frozen=True)
class BrowserCommand:
    action: BrowserAction
    url: str | None = None
    selector: str | None = None
    value: str | None = None

    def __post_init__(self) -> None:
        if self.url is not None and len(self.url) > 8_192:
            raise ValueError("browser URL is too long")
        if self.selector is not None and not self.selector.strip():
            raise ValueError("browser selector must not be blank")
        if self.selector is not None and len(self.selector) > 2_048:
            raise ValueError("browser selector is too long")
        if self.value is not None and len(self.value) > 64 * 1024:
            raise ValueError("browser value exceeds 64 KiB")


class BrowserWorker(Protocol):
    def execute(self, command: BrowserCommand) -> str: ...


class BrowserWorkerTool(Tool):
    metadata = ToolMetadata(
        name="browser_worker",
        description="Execute browser commands through an isolated worker",
        risk_level="high",
        requires_network=True,
        requires_approval=True,
    )

    def __init__(self, policy: BrowserPolicy, worker: BrowserWorker):
        self.policy = policy
        self.worker = worker

    def run(self, arguments):
        try:
            action = BrowserAction(arguments["action"])
            url = arguments.get("url")
            if url:
                url = self.policy.validate_url(url)

            selector = arguments.get("selector")
            value = arguments.get("value")

            if action is BrowserAction.NAVIGATE:
                if not url:
                    raise ValueError("navigate requires url")
                if selector is not None or value is not None:
                    raise ValueError("navigate does not accept selector or value")
            elif action is BrowserAction.READ:
                if value is not None:
                    raise ValueError("read does not accept value")
            elif action in {BrowserAction.CLICK, BrowserAction.SUBMIT}:
                if not selector:
                    raise ValueError(f"{action.value} requires selector")
                if value is not None:
                    raise ValueError(f"{action.value} does not accept value")
            elif action is BrowserAction.TYPE:
                if not selector:
                    raise ValueError("type requires selector")
                if value is None:
                    raise ValueError("type requires value")
            else:
                raise PermissionError(f"browser action is not implemented: {action.value}")

            command = BrowserCommand(action, url, selector, value)
            return ToolResult(success=True, output=self.worker.execute(command))
        except (KeyError, TypeError, ValueError, PermissionError) as exc:
            return ToolResult(success=False, error=str(exc))
