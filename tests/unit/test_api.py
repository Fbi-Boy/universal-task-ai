from backend.api.main import AnalyzeRequest, analyze_task, health


def test_health() -> None:
    assert health() == {"status": "ok"}


def test_analyze_task() -> None:
    response = analyze_task(AnalyzeRequest(task="buat laporan"))
    assert response.analysis.normalized_goal == "buat laporan"


def test_analyze_rejects_unknown_fields() -> None:
    try:
        AnalyzeRequest(task="buat laporan", admin=True)
    except ValueError:
        return
    raise AssertionError("unknown request fields were accepted")
