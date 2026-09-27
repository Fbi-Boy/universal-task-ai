from __future__ import annotations

import secrets
from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

MAX_REQUEST_ID_LENGTH = 128
DEFAULT_MAX_BODY_BYTES = 1_048_576

def _safe_request_id(value: str | None) -> str:
    if value is None:
        return secrets.token_hex(16)
    candidate = value.strip()
    if not candidate or len(candidate) > MAX_REQUEST_ID_LENGTH:
        return secrets.token_hex(16)
    if any(ord(char) < 33 or ord(char) > 126 for char in candidate):
        return secrets.token_hex(16)
    return candidate

class RequestContextMiddleware:
    """Attach a bounded correlation id without trusting caller-controlled values."""
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in scope.get("headers", [])
        }
        request_id = _safe_request_id(headers.get("x-request-id"))
        scope = dict(scope)
        scope["uta.request_id"] = request_id
        async def send_with_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                raw_headers = list(message.get("headers", []))
                raw_headers.append((b"x-request-id", request_id.encode("ascii")))
                message = dict(message)
                message["headers"] = raw_headers
            await send(message)
        await self.app(scope, receive, send_with_id)

class _BodyTooLarge(Exception):
    pass

class RequestBodyLimitMiddleware:
    """Reject oversized HTTP request bodies before application parsing."""
    def __init__(self, app: ASGIApp, *, max_body_bytes: int = DEFAULT_MAX_BODY_BYTES) -> None:
        if max_body_bytes <= 0:
            raise ValueError("max_body_bytes must be positive")
        self.app = app
        self.max_body_bytes = max_body_bytes
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        content_length = next(
            (
                int(value.decode("ascii"))
                for key, value in scope.get("headers", [])
                if key.lower() == b"content-length" and value.isdigit()
            ),
            None,
        )
        if content_length is not None and content_length > self.max_body_bytes:
            response = JSONResponse({"detail": "request body too large"}, status_code=413, headers={"cache-control": "no-store"})
            await response(scope, receive, send)
            return
        received = 0
        async def limited_receive() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_body_bytes:
                    raise _BodyTooLarge
            return message
        try:
            await self.app(scope, limited_receive, send)
        except _BodyTooLarge:
            response = JSONResponse({"detail": "request body too large"}, status_code=413, headers={"cache-control": "no-store"})
            await response(scope, receive, send)

def request_id_from_request(request: Request) -> str:
    value = request.scope.get("uta.request_id")
    return value if isinstance(value, str) and value else _safe_request_id(None)

def internal_error_response(request_id: str) -> Response:
    return JSONResponse(
        {"detail": "internal server error", "request_id": request_id},
        status_code=500,
        headers={"cache-control": "no-store"},
    )
