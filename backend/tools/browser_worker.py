from dataclasses import dataclass
from typing import Protocol
from backend.core.browser_policy import BrowserAction,BrowserPolicy
from backend.core.tools import Tool,ToolMetadata,ToolResult

@dataclass(frozen=True)
class BrowserCommand:
    action: BrowserAction
    url: str|None=None
    selector: str|None=None
    value: str|None=None

class BrowserWorker(Protocol):
    def execute(self, command: BrowserCommand) -> str: ...

class BrowserWorkerTool(Tool):
    metadata=ToolMetadata(name="browser_worker",description="Execute browser commands through an isolated worker",risk_level="high",requires_network=True,requires_approval=True)
    def __init__(self,policy:BrowserPolicy,worker:BrowserWorker):
        self.policy=policy; self.worker=worker
    def run(self,arguments):
        try:
            action=BrowserAction(arguments["action"])
            url=arguments.get("url")
            if url: url=self.policy.validate_url(url)
            if action is BrowserAction.NAVIGATE and not url: raise ValueError("navigate requires url")
            command=BrowserCommand(action,url,arguments.get("selector"),arguments.get("value"))
            return ToolResult(success=True,output=self.worker.execute(command))
        except (KeyError,ValueError,PermissionError) as exc:
            return ToolResult(success=False,error=str(exc))
