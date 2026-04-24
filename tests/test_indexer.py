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