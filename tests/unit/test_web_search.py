import pytest

from backend.tools.web_search import SearchResult, validate_search_query


def test_search_query_is_normalized() -> None:
    assert validate_search_query("  python  ") == "python"


def test_empty_search_query_rejected() -> None:
    with pytest.raises(ValueError):
        validate_search_query(" ")


def test_search_query_length_bounded() -> None:
    with pytest.raises(ValueError):
        validate_search_query("x" * 2001)


def test_search_result_is_typed() -> None:
    result = SearchResult("title", "https://example.com", "snippet")
    assert result.url == "https://example.com"
