"""
test_search.py

Unit tests for search.py.

These tests verify word lookup, query processing,
multi-word search, and edge-case behaviour.
"""

from src.search import format_word_entry, get_word_entry


SAMPLE_INDEX = {
    "life": {
        "document_frequency": 2,
        "pages": {
            "page1": {
                "frequency": 2,
                "positions": [0, 4],
            },
            "page2": {
                "frequency": 1,
                "positions": [3],
            },
        },
    },
    "good": {
        "document_frequency": 2,
        "pages": {
            "page1": {
                "frequency": 1,
                "positions": [1],
            },
            "page3": {
                "frequency": 1,
                "positions": [2],
            },
        },
    },
    "friends": {
        "document_frequency": 2,
        "pages": {
            "page1": {
                "frequency": 1,
                "positions": [2],
            },
            "page3": {
                "frequency": 1,
                "positions": [5],
            },
        },
    },
}


def test_get_word_entry_returns_existing_word():
    """
    Existing word should return its index entry.
    """
    result = get_word_entry(SAMPLE_INDEX, "life")

    assert result == SAMPLE_INDEX["life"]


def test_get_word_entry_returns_none_for_missing_word():
    """
    Missing word should return None.
    """
    result = get_word_entry(SAMPLE_INDEX, "unknown")

    assert result is None


def test_get_word_entry_is_case_insensitive():
    """
    Lookup should use the same tokenizer as indexing.
    """
    result = get_word_entry(SAMPLE_INDEX, "LIFE")

    assert result == SAMPLE_INDEX["life"]


def test_format_word_entry_returns_display_friendly_structure():
    """
    Formatter should return word, document frequency, and pages.
    """
    result = format_word_entry(SAMPLE_INDEX, "life")

    assert result == {
        "word": "life",
        "document_frequency": 2,
        "pages": SAMPLE_INDEX["life"]["pages"],
    }

from src.search import find_query


def test_find_query_single_word_returns_matching_pages():
    """
    Single-word query should return all pages containing that word.
    """
    result = find_query(SAMPLE_INDEX, "life")

    assert result == ["page1", "page2"]


def test_find_query_multi_word_returns_intersection():
    """
    Multi-word query should return only pages containing all query terms.
    """
    result = find_query(SAMPLE_INDEX, "good friends")

    assert result == ["page1", "page3"]


def test_find_query_returns_empty_list_if_one_term_missing():
    """
    If any query term is missing, no pages should match.
    """
    result = find_query(SAMPLE_INDEX, "good missingword")

    assert result == []

def test_find_query_is_case_insensitive():
    """
    Query matching should be case-insensitive.
    """
    result = find_query(SAMPLE_INDEX, "GOOD FRIENDS")

    assert result == ["page1", "page3"]


def test_find_query_handles_punctuation_heavy_query():
    """
    Query tokenizer should remove punctuation before searching.
    """
    result = find_query(SAMPLE_INDEX, "good!!! friends???")

    assert result == ["page1", "page3"]


def test_find_query_empty_query_returns_empty_list():
    """
    Empty query should return no results.
    """
    result = find_query(SAMPLE_INDEX, "")

    assert result == []


def test_find_query_punctuation_only_query_returns_empty_list():
    """
    Query with no valid tokens should return no results.
    """
    result = find_query(SAMPLE_INDEX, "!!! ??? ...")

    assert result == []


def test_find_query_repeated_terms_do_not_change_results():
    """
    Repeated query terms should not break or alter results.
    """
    result = find_query(SAMPLE_INDEX, "life life")

    assert result == ["page1", "page2"]

from src.search import get_pages_for_term, get_query_summary


def test_get_pages_for_term_returns_page_set():
    """
    get_pages_for_term should return a set of pages for a term.
    """
    result = get_pages_for_term(SAMPLE_INDEX, "life")

    assert result == {"page1", "page2"}


def test_get_pages_for_term_returns_empty_set_for_missing_term():
    """
    Missing term should return an empty page set.
    """
    result = get_pages_for_term(SAMPLE_INDEX, "missing")

    assert result == set()


def test_get_query_summary_returns_match_count_and_pages():
    """
    Query summary should return count and pages.
    """
    results = ["page1", "page2"]

    summary = get_query_summary(results)

    assert summary == {
        "match_count": 2,
        "pages": ["page1", "page2"],
    }