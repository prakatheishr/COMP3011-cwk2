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


def test_loaded_index_returns_no_results_for_missing_query(tmp_path):
    """
    Loaded index should return an empty result list for a query
    where one or more terms do not exist.
    """
    pages = [
        {
            "url": "page1",
            "content": "good friends",
        }
    ]

    index = build_index(pages)

    filepath = tmp_path / "index.json"
    save_index(index, str(filepath))
    loaded_index = load_index(str(filepath))

    results = find_query(loaded_index, "good missingword")

    assert results == []


from src.main import handle_find, handle_print


def test_handle_print_without_index_does_not_crash(capsys):
    """
    CLI print handler should handle missing in-memory index gracefully.
    """
    handle_print(None, "life")

    captured = capsys.readouterr()

    assert "No index loaded" in captured.out


def test_handle_find_without_index_does_not_crash(capsys):
    """
    CLI find handler should handle missing in-memory index gracefully.
    """
    handle_find(None, "life")

    captured = capsys.readouterr()

    assert "No index loaded" in captured.out


def test_handle_print_after_index_loaded_outputs_word_entry(capsys):
    """
    CLI print handler should display a word entry when an index is available.
    """
    pages = [
        {
            "url": "page1",
            "content": "life life good",
        }
    ]

    index = build_index(pages)

    handle_print(index, "life")

    captured = capsys.readouterr()

    assert "Word 'life' found" in captured.out
    assert "document_frequency" in captured.out


def test_handle_find_after_index_loaded_outputs_matching_pages(capsys):
    """
    CLI find handler should display matching page URLs when an index is available.
    """
    pages = [
        {
            "url": "page1",
            "content": "good friends",
        },
        {
            "url": "page2",
            "content": "good only",
        },
    ]

    index = build_index(pages)

    handle_find(index, "good friends")

    captured = capsys.readouterr()

    assert "Query 'good friends' matched" in captured.out
    assert "page1" in captured.out
    assert "page2" not in captured.out