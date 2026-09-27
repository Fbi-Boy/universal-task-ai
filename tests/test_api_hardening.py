from __future__ import annotations

import asyncio

from backend.api.hardening import RequestBodyLimitMiddleware, RequestContextMiddleware, SecurityHeadersMiddleware, _safe_request_id

def test_request_id_rejects_control_characters_and_bounds() -> None:
    generated = _safe_request_id("\n")
    assert generated != "\n"
    assert len(generated) == 32
    generated = _safe_request_id("x" * 129)
    assert len(generated) == 32
    assert _safe_request_id("client-123") == "client-123"

def test_request_body_limit_rejects_known_oversize() -> None:
    sent = []
    async def app(scope, receive, send):
        sent.append("called")
    middleware = RequestBodyLimitMiddleware(app, max_body_bytes=4)
    async def receive():
        return {"type": "http.request", "body": b"12345", "more_body": False}
    async def send(message):
        sent.append(message)
    asyncio.run(middleware(
        {"type": "http", "headers": [(b"content-length", b"5")], "method": "POST", "path": "/"},
        receive, send,
    ))
    assert "called" not in sent
    assert sent[0]["status"] == 413

def test_request_context_adds_bounded_correlation_id() -> None:
    received = []
    async def app(scope, receive, send):
        received.append(scope["uta.request_id"])
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})
    middleware = RequestContextMiddleware(app)
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}
    sent = []
    async def send(message):
        sent.append(message)
    asyncio.run(middleware(
        {"type": "http", "headers": [(b"x-request-id", b"client-123")], "method": "GET", "path": "/"},
        receive, send,
    ))
    assert received == ["client-123"]
    assert (b"x-request-id", b"client-123") in sent[0]["headers"]


def test_security_headers_are_added_without_overwriting_existing_values() -> None:
    async def app(scope, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"x-frame-options", b"SAMEORIGIN")],
        })
        await send({"type": "http.response.body", "body": b"ok"})

    middleware = SecurityHeadersMiddleware(app)

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    sent = []

    async def send(message):
        sent.append(message)

    asyncio.run(middleware(
        {"type": "http", "headers": [], "method": "GET", "path": "/"},
        receive,
        send,
    ))

    headers = dict(sent[0]["headers"])
    assert headers[b"x-content-type-options"] == b"nosniff"
    assert headers[b"x-frame-options"] == b"SAMEORIGIN"
    assert headers[b"referrer-policy"] == b"no-referrer"
