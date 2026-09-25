from pathlib import Path

def test_security_workflow_runs_security_suite():
    workflow=Path(".github/workflows/security.yml").read_text()
    assert "tests/security" in workflow
    assert "pip check" in workflow
    assert "compileall" in workflow
