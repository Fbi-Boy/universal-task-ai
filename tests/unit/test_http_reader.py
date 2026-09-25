from pathlib import Path
import pytest
from backend.core.network_policy import NetworkPolicy
from backend.core.egress import EgressPolicy
from backend.tools.http_reader import SafeHttpReader

def test_reader_rejects_private_resolution():
    reader=SafeHttpReader(NetworkPolicy(),egress=EgressPolicy(frozenset({"example.com","internal.example"})),resolver=lambda *args,**kwargs:[(None,None,None,None,("127.0.0.1",0))])
    with pytest.raises(PermissionError):
        reader.read("https://example.com")

def test_reader_rejects_redirect_to_private_target(monkeypatch):
    reader=SafeHttpReader(NetworkPolicy(),egress=EgressPolicy(frozenset({"example.com","internal.example"})),resolver=lambda host,port,**kwargs:[(None,None,None,None,("93.184.216.34",port))])
    monkeypatch.setattr(reader,"_resolve",lambda host,port:("93.184.216.34",) if host=="example.com" else ("10.0.0.1",))
    class FakeResponse:
        status=302
        def getheader(self,name): return "https://internal.example/" if name=="Location" else None
        def read(self,*args): return b""
    class FakeConn:
        def __init__(self,*args,**kwargs): pass
        def putrequest(self,*args,**kwargs): pass
        def putheader(self,*args,**kwargs): pass
        def endheaders(self): pass
        def getresponse(self): return FakeResponse()
        def close(self): pass
    monkeypatch.setattr("backend.tools.http_reader.http.client.HTTPConnection",FakeConn)
    monkeypatch.setattr("backend.tools.http_reader.socket.create_connection",lambda *a,**k:object())
    monkeypatch.setattr("backend.tools.http_reader.ssl.create_default_context",lambda:type("C",(),{"wrap_socket":lambda self,sock,server_hostname:sock})())
    with pytest.raises(PermissionError):
        reader.read("https://example.com")
