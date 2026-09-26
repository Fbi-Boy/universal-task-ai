from backend.core.browser_policy import BrowserAction, BrowserPolicy
from backend.tools.browser_worker import BrowserCommand
from backend.tools.playwright_worker import PlaywrightBrowserWorker


def test_playwright_worker_rejects_non_allowlisted_navigation_without_launch() -> None:
    worker = PlaywrightBrowserWorker(BrowserPolicy(frozenset({"allowed.example"})))
    try:
        worker.execute(BrowserCommand(BrowserAction.NAVIGATE, "https://evil.example"))
    except PermissionError:
        pass
    else:
        raise AssertionError("disallowed browser navigation must fail closed")
    assert worker._page is None


def test_playwright_worker_keeps_unimplemented_actions_denied_without_launch() -> None:
    worker = PlaywrightBrowserWorker(BrowserPolicy(frozenset({"allowed.example"})))
    for action in (
        BrowserAction.UPLOAD,
        BrowserAction.DOWNLOAD,
        BrowserAction.LOGIN,
        BrowserAction.PAYMENT,
    ):
        try:
            worker.execute(BrowserCommand(action, "https://allowed.example"))
        except PermissionError:
            pass
        else:
            raise AssertionError(f"{action.value} must remain denied")
    assert worker._page is None
