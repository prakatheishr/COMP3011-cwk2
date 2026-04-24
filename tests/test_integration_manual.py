"""
test_integration_manual.py

Temporary manual integration test for the full coursework workflow.
This script checks that crawling, indexing, saving, loading, and searching
all work together correctly.
"""

from src.crawler import crawl_site
from src.indexer import build_index, load_index, save_index
from src.main import INDEX_FILEPATH, START_URL
from src.search import find_query, format_word_entry


def main() -> None:
    """
    Run a manual end-to-end integration check.
    """
    print("=" * 60)
    print("MANUAL INTEGRATION TEST")
    print("=" * 60)

    # Step 1: crawl the site
    pages = crawl_site(START_URL)
    print(f"[INFO] Pages crawled: {len(pages)}")

    if not pages:
        print("[ERROR] No pages were crawled.")
        return

    # Step 2: build the index
    index = build_index(pages)
    print(f"[INFO] Unique terms indexed: {len(index)}")

    if not index:
        print("[ERROR] Index build failed.")
        return

    # Step 3: save the index
    save_index(index, INDEX_FILEPATH)
    print(f"[INFO] Index saved to: {INDEX_FILEPATH}")

    # Step 4: load the index
    loaded_index = load_index(INDEX_FILEPATH)
    if loaded_index is None:
        print("[ERROR] Failed to load saved index.")
        return

    print(f"[INFO] Loaded index terms: {len(loaded_index)}")

    # Step 5: verify round-trip consistency
    if loaded_index == index:
        print("[SUCCESS] Loaded index matches original index")
    else:
        print("[ERROR] Loaded index does not match original index")
        return

    # Step 6: test print-style lookup
    life_entry = format_word_entry(loaded_index, "life")
    if life_entry is not None:
        print("[SUCCESS] Print-style lookup for 'life' worked")
    else:
        print("[ERROR] Print-style lookup for 'life' failed")

    # Step 7: test find-style query
    query_results = find_query(loaded_index, "good friends")
    print(f"[INFO] Query results for 'good friends': {query_results}")

    if query_results:
        print("[SUCCESS] Find-style multi-word search worked")
    else:
        print("[ERROR] Find-style multi-word search returned no results")

    print("=" * 60)
    print("MANUAL INTEGRATION TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()