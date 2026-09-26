import pytest
from backend.core.browser_policy import BrowserPolicy,BrowserAction
from backend.tools.browser_session import BrowserSession

def test_session_revalidates_redirects():
    s=BrowserSession(BrowserPolicy(frozenset({"editor.example"})),"s1")
    assert s.navigate("https://editor.example")=="https://editor.example"
    with pytest.raises(PermissionError): s.validate_redirect("https://evil.example")

def test_sensitive_action_is_marked_for_approval():
    s=BrowserSession(BrowserPolicy(frozenset({"editor.example"})),"s1")
    assert s.check_action(BrowserAction.LOGIN)
