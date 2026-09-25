from backend.core.reviewer import Reviewer


def test_reviewer_passes_valid_output() -> None:
    result = Reviewer().review({"ok": True}, [lambda value: value["ok"]])
    assert result.passed
    assert not result.failures


def test_reviewer_reports_failed_check() -> None:
    result = Reviewer().review("bad", [lambda value: False])
    assert not result.passed
    assert len(result.failures) == 1
