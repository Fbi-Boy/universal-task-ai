from backend.core.runtime import RuntimeComposition, RuntimeServices

def test_runtime_requires_all_services():
    s=RuntimeServices(object(),object(),object(),object())
    assert RuntimeComposition(s).validate() is s

def test_runtime_rejects_missing_service():
    try:
        RuntimeComposition(RuntimeServices(None,object(),object(),object())).validate()
        assert False
    except ValueError as exc:
        assert "task_dispatcher" in str(exc)
