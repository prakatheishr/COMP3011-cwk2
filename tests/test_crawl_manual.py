"""
test_crawl_manual.py

Temporary manual test script for crawler development.
This is useful during implementation before proper pytest tests are added.
"""

from src.crawler import crawl_site

def main() -> None:
    """
    Run a quick manual crawler check and print a summary of results.
    """
    pages = crawl_site("https://quotes.toscrape.com/")

    print(f"Total pages crawled: {len(pages)}")
    print(f"First page URL: {pages[0]['url']}")
    print(f"First page number: {pages[0]['page_number']}")
    print(f"Number of quotes on first page: {len(pages[0]['quotes'])}")
    print(f"Content preview: {pages[0]['content'][:200]}")


if __name__ == "__main__":
    main()