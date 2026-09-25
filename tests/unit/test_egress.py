import pytest
from backend.core.egress import EgressPolicy

def test_allowed_host_and_port(): EgressPolicy(frozenset({"api.example.com"})).authorize("API.EXAMPLE.COM.",443)
def test_unlisted_host_denied():
    with pytest.raises(PermissionError): EgressPolicy(frozenset({"api.example.com"})).authorize("evil.example",443)
def test_port_denied():
    with pytest.raises(PermissionError): EgressPolicy(frozenset({"api.example.com"})).authorize("api.example.com",80)
def test_literal_ip_denied():
    with pytest.raises(PermissionError): EgressPolicy(frozenset({"api.example.com"})).authorize("93.184.216.34",443)
