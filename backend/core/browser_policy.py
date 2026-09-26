"""Policy boundary for browser-agent actions.

This module does not drive a browser. It defines the safety contract that a
future browser worker must enforce before navigation or side effects.
"""
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse


class BrowserAction(str, Enum):
    NAVIGATE = "navigate"
    READ = "read"
    CLICK = "click"
    TYPE = "type"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    SUBMIT = "submit"
    LOGIN = "login"
    PAYMENT = "payment"


@dataclass(frozen=True)
class BrowserPolicy:
    allowed_hosts: frozenset[str]
    max_download_bytes: int = 20 * 1024 * 1024

    def validate_url(self, url: str) -> str:
        if not url or any(c.isspace() for c in url):
            raise ValueError("invalid browser URL")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("browser navigation requires HTTPS")
        if parsed.username or parsed.password:
            raise ValueError("credentials in browser URLs are forbidden")
        host = parsed.hostname.lower().rstrip(".")
        if host not in self.allowed_hosts:
            raise PermissionError("browser host is not allowlisted")
        return parsed.geturl()

    def requires_approval(self, action: BrowserAction) -> bool:
        return action in {
            BrowserAction.TYPE,
            BrowserAction.UPLOAD,
            BrowserAction.SUBMIT,
            BrowserAction.LOGIN,
            BrowserAction.PAYMENT,
        }

    def validate_download_size(self, size: int) -> None:
        if size < 0 or size > self.max_download_bytes:
            raise ValueError("browser download exceeds policy limit")
