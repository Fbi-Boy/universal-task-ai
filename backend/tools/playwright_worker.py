from dataclasses import dataclass
from typing import Any

from backend.core.browser_policy import BrowserAction, BrowserPolicy
from backend.tools.browser_worker import BrowserCommand, BrowserWorker


@dataclass
class PlaywrightBrowserWorker(BrowserWorker):
    """Minimal browser worker: allowlisted HTTPS navigation and bounded reads."""

    policy: BrowserPolicy
    max_output_chars: int = 256_000

    def __post_init__(self) -> None:
        if self.max_output_chars < 1 or self.max_output_chars > 1_000_000:
            raise ValueError("max_output_chars must be between 1 and 1000000")
        self._playwright = None
        self._browser = None
        self._page = None

    def _ensure_page(self) -> Any:
        if self._page is not None:
            return self._page
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError("browser capability requires the optional playwright dependency") from exc

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=True)
        context = self._browser.new_context(accept_downloads=False)

        def guard(route: Any) -> None:
            try:
                self.policy.validate_url(route.request.url)
            except (ValueError, PermissionError):
                route.abort()
                return
            route.continue_()

        context.route("**/*", guard)
        self._page = context.new_page()
        return self._page

    def execute(self, command: BrowserCommand) -> str:
        if command.action not in {BrowserAction.NAVIGATE, BrowserAction.READ}:
            raise PermissionError("browser worker currently permits only navigate and read")
        if command.url is not None:
            command = BrowserCommand(
                command.action,
                self.policy.validate_url(command.url),
                command.selector,
                command.value,
            )
        page = self._ensure_page()

        if command.action is BrowserAction.NAVIGATE:
            if not command.url:
                raise ValueError("navigate requires url")
            page.goto(command.url, wait_until="domcontentloaded", timeout=20_000)
            self.policy.validate_url(page.url)
            return page.url

        self.policy.validate_url(page.url)
        if command.selector:
            text = page.locator(command.selector).inner_text(timeout=10_000)
        else:
            text = page.locator("body").inner_text(timeout=10_000)
        return text[: self.max_output_chars]

    def close(self) -> None:
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()
        self._browser = None
        self._page = None
        self._playwright = None
