from dataclasses import dataclass
from backend.core.browser_policy import BrowserAction,BrowserPolicy

@dataclass
class BrowserSession:
    policy: BrowserPolicy
    session_id: str
    current_url: str|None = None

    def navigate(self,url:str)->str:
        safe=self.policy.validate_url(url)
        self.current_url=safe
        return safe

    def validate_redirect(self,url:str)->str:
        return self.policy.validate_url(url)

    def check_action(self,action:BrowserAction)->bool:
        return self.policy.requires_approval(action)
