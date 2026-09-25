import http.client
import json
import socket
import ssl
from typing import Any, Mapping
from urllib.parse import urljoin, urlparse

from backend.core.egress import EgressPolicy
from backend.core.network_policy import NetworkPolicy
from backend.core.tools import Tool, ToolMetadata, ToolResult


class SafeHttpReader(Tool):
    metadata = ToolMetadata(name="http_reader", description="Read a bounded HTTPS response with DNS/IP and egress policy enforcement", risk_level="medium", requires_network=True, requires_approval=True)

    def __init__(self, policy: NetworkPolicy, *, egress: EgressPolicy, resolver=None) -> None:
        self._policy, self._egress, self._resolver = policy, egress, resolver or socket.getaddrinfo

    def _resolve(self, host: str, port: int) -> tuple[str, ...]:
        infos = self._resolver(host, port, type=socket.SOCK_STREAM)
        addresses = tuple(dict.fromkeys(info[4][0] for info in infos))
        if not addresses:
            raise PermissionError("hostname did not resolve")
        return addresses

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        url = arguments.get("url")
        if not isinstance(url, str) or not url.strip():
            return ToolResult(success=False, error="url must be a non-empty string")
        try:
            return ToolResult(success=True, output=self.read(url))
        except (PermissionError, ValueError, OSError, TimeoutError) as exc:
            return ToolResult(success=False, error=str(exc))

    def read(self, url: str) -> dict[str, Any]:
        return self._request(url)

    def read_with_headers(self, url: str, *, headers: Mapping[str, str]) -> dict[str, Any]:
        return self._request(url, headers=headers)

    def _request(self, url: str, *, headers: Mapping[str, str] | None = None) -> dict[str, Any]:
        current = url
        for redirect_count in range(self._policy.max_redirects + 1):
            parsed = urlparse(current)
            host = parsed.hostname
            if not host:
                raise PermissionError("URL hostname is required")
            port = parsed.port or 443
            self._egress.authorize(host, port)
            resolved = self._resolve(host, port)
            self._policy.validate_url(current, resolved_ips=resolved)
            target_ip = resolved[0]
            context = ssl.create_default_context()
            sock = socket.create_connection((target_ip, port), timeout=self._policy.timeout_seconds)
            conn = None
            try:
                sock = context.wrap_socket(sock, server_hostname=host)
                conn = http.client.HTTPConnection(host, port, timeout=self._policy.timeout_seconds)
                conn.sock = sock
                path = parsed.path or "/"
                path += ("?" + parsed.query) if parsed.query else ""
                conn.putrequest("GET", path, skip_host=True, skip_accept_encoding=True)
                conn.putheader("Host", host if parsed.port is None or port == 443 else f"{host}:{port}")
                conn.putheader("Accept", "text/plain, text/html, application/json")
                conn.putheader("Connection", "close")
                for key, value in (headers or {}).items():
                    conn.putheader(key, value)
                conn.endheaders()
                response = conn.getresponse()
                location = response.getheader("Location")
                if response.status in {301, 302, 303, 307, 308}:
                    if not location:
                        raise ValueError("redirect response missing Location")
                    if redirect_count >= self._policy.max_redirects:
                        raise PermissionError("redirect limit exceeded")
                    current = urljoin(current, location)
                    response.read(self._policy.max_response_bytes + 1)
                    conn.close()
                    continue
                body = response.read(self._policy.max_response_bytes + 1)
                if len(body) > self._policy.max_response_bytes:
                    raise ValueError("response exceeds configured size limit")
                content_type = response.getheader("Content-Type")
                result = {"status": response.status, "content_type": content_type, "body": body.decode("utf-8", errors="replace")}
                if content_type and "application/json" in content_type.lower():
                    try:
                        result["json"] = json.loads(result["body"])
                    except json.JSONDecodeError as exc:
                        raise ValueError("response contains invalid JSON") from exc
                return result
            finally:
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        pass
        raise PermissionError("redirect limit exceeded")
