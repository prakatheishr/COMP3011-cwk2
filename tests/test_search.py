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