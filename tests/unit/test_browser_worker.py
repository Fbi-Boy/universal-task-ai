from backend.core.browser_policy import BrowserPolicy
from backend.tools.browser_worker import BrowserWorkerTool


class FakeWorker:
    def __init__(self):
        self.calls = []

    def execute(self, command):
        self.calls.append(command)
        return "ok"


def test_worker_never_receives_disallowed_url():
    w = FakeWorker()
    t = BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})), w)
    r = t.run({"action": "navigate", "url": "https://evil.example"})
    assert not r.success and not w.calls


def test_worker_receives_allowlisted_navigation():
    w = FakeWorker()
    t = BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})), w)
    r = t.run({"action": "navigate", "url": "https://allowed.example/editor"})
    assert r.success and len(w.calls) == 1


def test_worker_validates_click_selector_before_worker():
    w = FakeWorker()
    t = BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})), w)
    r = t.run({"action": "click"})
    assert not r.success and not w.calls


def test_worker_accepts_bounded_type_command():
    w = FakeWorker()
    t = BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})), w)
    r = t.run({"action": "type", "selector": "#name", "value": "Fabi"})
    assert r.success and w.calls[0].selector == "#name"


def test_worker_rejects_oversized_selector():
    w = FakeWorker()
    t = BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})), w)
    r = t.run({"action": "click", "selector": "x" * 2_049})
    assert not r.success and not w.calls


def test_worker_keeps_credential_and_payment_actions_unimplemented():
    w = FakeWorker()
    t = BrowserWorkerTool(BrowserPolicy(frozenset({"allowed.example"})), w)
    for action in ("upload", "download", "login", "payment"):
        r = t.run({"action": action, "selector": "#x"})
        assert not r.success
    assert not w.calls
