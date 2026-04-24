"""
test_integration.py

Integration tests for the full search tool workflow.

These tests verify that crawler-style page records can be indexed,
saved, loaded, and searched successfully.
"""

from src.indexer import build_index, load_index, save_index
from src.search import find_query, format_word_entry


def test_build_save_load_and_search_workflow(tmp_path):
    """
    Full workflow:
    - build index from page records
    - save index to JSON
    - load index from JSON
    - run print-style lookup
    - run find-style search
    """
    pages = [
        {
            "url": "page1",
            "content": "life is good with friends",
        },
        {
            "url": "page2",
            "content": "life is different here",
        },
    ]

    index = build_index(pages)

    filepath = tmp_path / "index.json"
    save_index(index, str(filepath))

    loaded_index = load_index(str(filepath))

    assert loaded_index == index

    word_entry = format_word_entry(loaded_index, "life")
    assert word_entry is not None
    assert word_entry["document_frequency"] == 2

    results = find_query(loaded_index, "good friends")
    assert results == ["page1"]