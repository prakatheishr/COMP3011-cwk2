"""
test_indexer.py

Unit tests for indexer.py.

These tests verify tokenization, inverted index construction,
and JSON persistence behaviour.
"""

from src.indexer import tokenize


def test_tokenize_lowercases_text():
    """
    Tokenizer should convert all text to lowercase.
    """
    result = tokenize("Hello WORLD")

    assert result == ["hello", "world"]


def test_tokenize_removes_punctuation():
    """
    Tokenizer should remove punctuation and split into clean terms.
    """
    result = tokenize("Hello, world! Python-test.")

    assert result == ["hello", "world", "python", "test"]


def test_tokenize_handles_empty_string():
    """
    Empty input should return an empty token list.
    """
    result = tokenize("")

    assert result == []


def test_tokenize_handles_numbers():
    """
    Numbers should be kept because they may appear in page content.
    """
    result = tokenize("Page 10 has 2 quotes")

    assert result == ["page", "10", "has", "2", "quotes"]

from src.indexer import build_index


def test_build_index_stores_frequency_and_positions():
    """
    Index should store word frequency and token positions per page.
    """
    pages = [
        {
            "url": "page1",
            "content": "life is life",
        }
    ]

    index = build_index(pages)

    assert "life" in index
    assert index["life"]["document_frequency"] == 1
    assert index["life"]["pages"]["page1"]["frequency"] == 2
    assert index["life"]["pages"]["page1"]["positions"] == [0, 2]


def test_build_index_stores_document_frequency_once_per_page():
    """
    Document frequency should count pages, not total word occurrences.
    """
    pages = [
        {
            "url": "page1",
            "content": "life life life",
        },
        {
            "url": "page2",
            "content": "life again",
        },
    ]

    index = build_index(pages)

    assert index["life"]["document_frequency"] == 2
    assert index["life"]["pages"]["page1"]["frequency"] == 3
    assert index["life"]["pages"]["page2"]["frequency"] == 1


def test_build_index_handles_repeated_words():
    """
    Repeated words should increase frequency and store all positions.
    """
    pages = [
        {
            "url": "page1",
            "content": "good good friends",
        }
    ]

    index = build_index(pages)

    assert index["good"]["pages"]["page1"]["frequency"] == 2
    assert index["good"]["pages"]["page1"]["positions"] == [0, 1]

def test_build_index_handles_empty_content():
    """
    A page with empty content should not crash the indexer.
    """
    pages = [
        {
            "url": "page1",
            "content": "",
        }
    ]

    index = build_index(pages)

    assert index == {}


def test_build_index_skips_page_without_url():
    """
    Malformed page records without a URL should be skipped.
    """
    pages = [
        {
            "content": "life is good",
        }
    ]

    index = build_index(pages)

    assert index == {}


def test_build_index_handles_missing_content():
    """
    Page records with missing content should be treated as empty content.
    """
    pages = [
        {
            "url": "page1",
        }
    ]

    index = build_index(pages)

    assert index == {}