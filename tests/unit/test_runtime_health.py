from backend.core.runtime import RuntimeServices
from backend.core.runtime_health import RuntimeHealth

def test_health_is_ok_when_all_dependencies_exist():
    services = RuntimeServices(object(), object(), object(), object())
    report = RuntimeHealth(services).check()
    assert report.status == "ok"
    assert len(report.checks) == 4

def test_health_reports_degraded_for_missing_dependency():
    services = RuntimeServices(None, object(), object(), object())
    assert RuntimeHealth(services).check().status == "degraded"
