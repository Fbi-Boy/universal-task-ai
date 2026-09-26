import pytest
from backend.tools.download_policy import DownloadPolicy

def test_download_policy_bounds_type_and_path():
    p=DownloadPolicy()
    assert p.validate("report.pdf",100)
    with pytest.raises(PermissionError): p.validate("../secret.txt",100)
    with pytest.raises(PermissionError): p.validate("run.exe",100)
