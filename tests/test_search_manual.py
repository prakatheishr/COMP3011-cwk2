"""
test_search_manual.py

Temporary manual test script for search development.
This is useful during implementation before proper pytest tests are added.
"""

from src.crawler import crawl_site
from src.indexer import build_index, tokenize
from src.search import find_query, format_word_entry, get_word_entry


def main() -> None:
    """
    Crawl the site, build the index, and manually verify search behaviour.
    """
    # Crawl the site and build the index
    pages = crawl_site("https://quotes.toscrape.com/")
    index = build_index(pages)

    print("=" * 60)
    print("MANUAL SEARCH TESTS")
    print("=" * 60)

    # 1. Single-word lookup works
    print("\n[TEST 1] Single-word lookup works")
    word = "life"
    word_entry = get_word_entry(index, word)
    print(f"Lookup word: {word}")
    print(f"Result is None? {word_entry is None}")
    if word_entry is not None:
        print("PASS: single-word lookup returned an index entry")
        print(word_entry)
    else:
        print("FAIL: single-word lookup returned None")

    # 2. Missing word returns None
    print("\n[TEST 2] Missing word returns None")
    missing_word = "xyzabcnotaword"
    missing_entry = get_word_entry(index, missing_word)
    print(f"Lookup word: {missing_word}")
    print(f"Returned value: {missing_entry}")
    if missing_entry is None:
        print("PASS: missing word returned None")
    else:
        print("FAIL: missing word did not return None")

    # 3. Query tokenization uses the same tokenizer as indexing
    print("\n[TEST 3] Query tokenization uses the same tokenizer as indexing")
    raw_text = "Life, LIFE!! friends..."
    tokens = tokenize(raw_text)
    query_results = find_query(index, "Life, LIFE!!")
    print(f"Tokenized text: {tokens}")
    print(f"Query results for 'Life, LIFE!!': {query_results}")
    print("Check manually that tokenization lowercases and removes punctuation.")
    print("Expected relevant tokens to include: ['life', 'life', 'friends']")

    # 4. Single-word queries return all matching pages
    print("\n[TEST 4] Single-word queries return all matching pages")
    single_query = "life"
    single_results = find_query(index, single_query)
    print(f"Query: {single_query}")
    print(f"Matched pages ({len(single_results)}):")
    print(single_results)
    if single_results:
        print("PASS: single-word query returned matching pages")
    else:
        print("FAIL: single-word query returned no results")

    # 5. Multi-word queries return only intersecting pages
    print("\n[TEST 5] Multi-word queries return only intersecting pages")
    multi_query = "good friends"
    multi_results = find_query(index, multi_query)
    good_results = set(find_query(index, "good"))
    friends_results = set(find_query(index, "friends"))
    manual_intersection = sorted(good_results.intersection(friends_results))

    print(f"Query: {multi_query}")
    print(f"Search results: {multi_results}")
    print(f"Manual intersection: {manual_intersection}")

    if multi_results == manual_intersection:
        print("PASS: multi-word query matches the intersection of both terms")
    else:
        print("FAIL: multi-word query does not match the expected intersection")

    # 6. Repeated terms do not break search
    print("\n[TEST 6] Repeated terms do not break search")
    repeated_query = "life life"
    repeated_results = find_query(index, repeated_query)
    normal_results = find_query(index, "life")

    print(f"Results for repeated query '{repeated_query}': {repeated_results}")
    print(f"Results for normal query 'life': {normal_results}")

    if repeated_results == normal_results:
        print("PASS: repeated terms do not change the results incorrectly")
    else:
        print("FAIL: repeated terms produced unexpected results")

    # 7. Empty query returns an empty list
    print("\n[TEST 7] Empty query returns an empty list")
    empty_query = ""
    empty_results = find_query(index, empty_query)
    print(f"Query: '{empty_query}'")
    print(f"Returned value: {empty_results}")

    if empty_results == []:
        print("PASS: empty query returned an empty list")
    else:
        print("FAIL: empty query did not return an empty list")

    # 8. Results are returned in deterministic sorted order
    print("\n[TEST 8] Results are returned in deterministic sorted order")
    sorted_query = "life"
    sorted_results = find_query(index, sorted_query)
    manually_sorted_results = sorted(sorted_results)

    print(f"Search results: {sorted_results}")
    print(f"Manually sorted: {manually_sorted_results}")

    if sorted_results == manually_sorted_results:
        print("PASS: results are already sorted deterministically")
    else:
        print("FAIL: results are not returned in sorted order")

    # Optional extra: formatted entry check
    print("\n[EXTRA] Formatted word entry for CLI display")
    formatted_entry = format_word_entry(index, "life")
    print(formatted_entry)

    print("\n" + "=" * 60)
    print("MANUAL SEARCH TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()