from backend.core.runtime import RuntimeServices
from backend.core.runtime_health import RuntimeHealth

def test_health_is_ok_when_all_dependencies_exist():
    s=RuntimeServices(object(),object(),object(),object())
    r=RuntimeHealth(s).check()
    assert r.status=="ok" and len(r.checks)==4

def test_health_reports_degraded_for_missing_dependency():
    s=RuntimeServices(None,object(),object(),object())
    assert RuntimeHealth(s).check().status=="degraded"
