"""
test_indexer_manual.py

Temporary manual test script for indexer development.
This is useful during implementation before proper pytest tests are added.
"""

from src.crawler import crawl_site
from src.indexer import build_index


def main() -> None:
    """
    Crawl the quotes website, build the inverted index,
    and print a small summary for manual verification.
    """
    pages = crawl_site("https://quotes.toscrape.com/")
    index = build_index(pages)

    print(f"Total pages crawled: {len(pages)}")
    print(f"Total unique terms indexed: {len(index)}")

    # Print one sample term if it exists
    sample_term = "life"
    if sample_term in index:
        print(f"Sample term: {sample_term}")
        print(index[sample_term])
    else:
        print(f"Sample term '{sample_term}' was not found in the index.")


if __name__ == "__main__":
    main()