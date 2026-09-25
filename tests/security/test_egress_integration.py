import pytest
from backend.core.egress import EgressPolicy
from backend.core.network_policy import NetworkPolicy
from backend.tools.http_reader import SafeHttpReader

def test_http_reader_denies_unlisted_host():
    reader=SafeHttpReader(NetworkPolicy(),egress=EgressPolicy(frozenset({"allowed.example"})))
    result=reader.run({"url":"https://blocked.example/"})
    assert not result.success
    assert "egress host" in result.error

def test_http_reader_denies_unlisted_port():
    reader=SafeHttpReader(NetworkPolicy(),egress=EgressPolicy(frozenset({"allowed.example"})))
    result=reader.run({"url":"https://allowed.example:8443/"})
    assert not result.success
    assert "egress port" in result.error
