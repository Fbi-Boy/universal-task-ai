from dataclasses import dataclass
from typing import Protocol

from backend.core.browser_policy import BrowserAction, BrowserPolicy
from backend.core.tools import Tool, ToolMetadata, ToolResult

_MAX_COMMANDS = 8


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

    def _command(self, arguments: dict) -> BrowserCommand:
        allowed = {"action", "url", "selector", "value"}
        unknown = set(arguments) - allowed
        if unknown:
            raise ValueError(f"unknown browser command fields: {sorted(unknown)}")
        try:
            action = BrowserAction(arguments["action"])
        except KeyError as exc:
            raise ValueError("browser command requires action") from exc
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
        return BrowserCommand(action, url, selector, value)

    def run(self, arguments):
        try:
            if "commands" in arguments:
                commands = arguments["commands"]
                if not isinstance(commands, list) or not commands:
                    raise ValueError("commands must be a non-empty list")
                if len(commands) > _MAX_COMMANDS:
                    raise ValueError("browser command batch is limited to 8 commands")
                if any(not isinstance(item, dict) for item in commands):
                    raise ValueError("each browser command must be an object")
                parsed = tuple(self._command(item) for item in commands)
                execute_batch = getattr(self.worker, "execute_batch", None)
                if execute_batch is None:
                    raise RuntimeError("browser worker does not support isolated command batches")
                return ToolResult(success=True, output=execute_batch(parsed))
            return ToolResult(success=True, output=self.worker.execute(self._command(arguments)))
        except (KeyError, TypeError, ValueError, PermissionError, RuntimeError) as exc:
            return ToolResult(success=False, error=str(exc))
