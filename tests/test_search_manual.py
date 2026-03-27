"""
test_search_manual.py

Temporary manual test script for search development.
This is useful during implementation before proper pytest tests are added.
"""

from src.crawler import crawl_site
from src.indexer import build_index
from src.search import find_query, format_word_entry


def main() -> None:
    """
    Crawl the site, build the index, and manually verify search behaviour.
    """
    # Crawl the site and build the index
    pages = crawl_site("https://quotes.toscrape.com/")
    index = build_index(pages)

    # Test a single-word lookup
    word = "life"
    word_entry = format_word_entry(index, word)

    if word_entry is not None:
        print(f"[INFO] Word entry found for '{word}'")
        print(word_entry)
    else:
        print(f"[ERROR] Word '{word}' was not found")

    # Test a single-word query
    single_word_query = "life"
    single_word_results = find_query(index, single_word_query)
    print(f"[INFO] Results for query '{single_word_query}':")
    print(single_word_results)

    # Test a multi-word query
    multi_word_query = "good friends"
    multi_word_results = find_query(index, multi_word_query)
    print(f"[INFO] Results for query '{multi_word_query}':")
    print(multi_word_results)


if __name__ == "__main__":
    main()