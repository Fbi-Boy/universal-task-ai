import hashlib
import hmac

def verify_webhook_signature(body: bytes, signature: str, app_secret: str) -> bool:
    """Verify provider signature without logging or returning secret material."""
    if not signature.startswith("sha256="):
        return False
    supplied=signature.removeprefix("sha256=")
    expected=hmac.new(app_secret.encode(),body,hashlib.sha256).hexdigest()
    return hmac.compare_digest(supplied,expected)

def verify_challenge(token: str, expected_token: str, challenge: str) -> str:
    if not hmac.compare_digest(token,expected_token):
        raise PermissionError("webhook verification token mismatch")
    return challenge
