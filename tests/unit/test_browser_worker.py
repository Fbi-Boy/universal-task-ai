from backend.core.browser_policy import BrowserPolicy
from backend.tools.browser_worker import BrowserWorkerTool

class FakeWorker:
    def __init__(self): self.calls=[]
    def execute(self,command): self.calls.append(command); return "ok"

def test_worker_never_receives_disallowed_url():
    w=FakeWorker(); t=BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})),w)
    r=t.run({"action":"navigate","url":"https://evil.example"})
    assert not r.success and not w.calls

def test_worker_receives_allowlisted_navigation():
    w=FakeWorker(); t=BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})),w)
    r=t.run({"action":"navigate","url":"https://allowed.example/editor"})
    assert r.success and len(w.calls)==1
