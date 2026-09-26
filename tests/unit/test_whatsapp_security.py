import hashlib,hmac
import pytest
from backend.channels.whatsapp_security import verify_webhook_signature,verify_challenge

def test_signature_verification():
    body=b'{"messages":[]}'
    secret="secret"
    digest=hmac.new(secret.encode(),body,hashlib.sha256).hexdigest()
    assert verify_webhook_signature(body,"sha256="+digest,secret)
    assert not verify_webhook_signature(body,"sha256=bad",secret)

def test_challenge_requires_expected_token():
    assert verify_challenge("token","token","123")=="123"
    with pytest.raises(PermissionError): verify_challenge("bad","token","123")
