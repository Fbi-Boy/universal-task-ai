import pytest
from backend.core.browser_policy import BrowserAction, BrowserPolicy

def test_browser_policy_allows_allowlisted_https():
    p=BrowserPolicy(frozenset({'example.edu'}))
    assert p.validate_url('https://example.edu/tasks') == 'https://example.edu/tasks'

@pytest.mark.parametrize('url',['http://example.edu','file:///tmp/secret','javascript:alert(1)','https://evil.example','https://user:pass@example.edu'])
def test_browser_policy_rejects_unsafe_urls(url):
    with pytest.raises((ValueError,PermissionError)): BrowserPolicy(frozenset({'example.edu'})).validate_url(url)

def test_sensitive_browser_actions_require_approval():
    p=BrowserPolicy(frozenset({'example.edu'}))
    assert p.requires_approval(BrowserAction.LOGIN)
    assert p.requires_approval(BrowserAction.SUBMIT)
    assert not p.requires_approval(BrowserAction.READ)

def test_download_limit():
    p=BrowserPolicy(frozenset({'example.edu'}),max_download_bytes=10)
    p.validate_download_size(10)
    with pytest.raises(ValueError): p.validate_download_size(11)
