from scripts.smoke_local import request


def test_smoke_module_imports():
    assert callable(request)
