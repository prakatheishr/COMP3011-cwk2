"""
crawler.py

Core crawler logic for the COMP3011 coursework search tool.

This module is responsible for:
- downloading pages from quotes.toscrape.com
- extracting quote content from each page
- following pagination links
- returning structured page records for indexing
- enforcing a politeness delay between requests
"""

from urllib.parse import urljoin
import time

import requests
from bs4 import BeautifulSoup


def wait_if_needed(last_request_time: float | None, delay: int = 6) -> None:
    """
    Enforce a minimum delay between HTTP requests.

    Parameters:
        last_request_time (float | None): Timestamp of the previous request,
            or None if no request has been made yet.
        delay (int): Minimum number of seconds required between requests.
    """
    # If this is the first request, there is nothing to wait for
    if last_request_time is None:
        return

    # Calculate how much time has passed since the previous request
    elapsed_time = time.time() - last_request_time

    # Only sleep if less than the required delay has passed
    if elapsed_time < delay:
        time.sleep(delay - elapsed_time)


def fetch_page(url: str) -> str | None:
    """
    Download a page and return its HTML content.

    Parameters:
        url (str): The URL to fetch.

    Returns:
        str | None:
            Raw HTML content of the page if successful,
            otherwise None if the request fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.Timeout:
        print(f"[ERROR] Request timed out while fetching: {url}")
        return None

    except requests.HTTPError as error:
        print(f"[ERROR] HTTP error while fetching {url}: {error}")
        return None

    except requests.RequestException as error:
        print(f"[ERROR] Network error while fetching {url}: {error}")
        return None


def parse_page(html: str, url: str, page_number: int) -> dict:
    """
    Parse a quotes.toscrape.com page into a structured page record.

    Parameters:
        html (str): Raw HTML content of the page.
        url (str): URL of the current page.
        page_number (int): Page number in the crawl sequence.

    Returns:
        dict: Structured page record containing:
            - url
            - page_number
            - content
            - quotes
    """
    soup = BeautifulSoup(html, "html.parser")

    # Find all quote containers on the page
    quote_blocks = soup.find_all("div", class_="quote")

    quotes = []
    content_parts = []

    # Extract text, author, and tags from each quote block
    for block in quote_blocks:
        text_tag = block.find("span", class_="text")
        author_tag = block.find("small", class_="author")
        tag_elements = block.find_all("a", class_="tag")

        quote_text = text_tag.get_text(strip=True) if text_tag else ""
        author = author_tag.get_text(strip=True) if author_tag else ""
        tags = [tag.get_text(strip=True) for tag in tag_elements]

        quotes.append(
            {
                "text": quote_text,
                "author": author,
                "tags": tags,
            }
        )

        # Build a combined content string for later indexing
        if quote_text:
            content_parts.append(quote_text)
        if author:
            content_parts.append(author)
        if tags:
            content_parts.extend(tags)

    combined_content = " ".join(content_parts)

    return {
        "url": url,
        "page_number": page_number,
        "content": combined_content,
        "quotes": quotes,
    }


def find_next_page(html: str, current_url: str) -> str | None:
    """
    Find the URL of the next page in the pagination sequence.

    Parameters:
        html (str): Raw HTML of the current page.
        current_url (str): URL of the current page.

    Returns:
        str | None: Absolute URL of the next page, or None if no next page exists.
    """
    soup = BeautifulSoup(html, "html.parser")

    # quotes.toscrape.com stores the next-page link inside:
    # <li class="next"><a href="/page/2/">Next →</a></li>
    next_li = soup.find("li", class_="next")

    if not next_li:
        return None

    next_link = next_li.find("a")
    if not next_link or "href" not in next_link.attrs:
        return None

    # Convert the relative link into an absolute URL
    return urljoin(current_url, next_link["href"])


def crawl_site(start_url: str) -> list[dict]:
    """
    Crawl the website from the starting URL until no next page exists.

    Parameters:
        start_url (str): The first page to crawl.

    Returns:
        list[dict]: A list of structured page records.
    """
    crawled_pages = []
    current_url = start_url
    page_number = 1
    last_request_time = None

    while current_url:
        # Enforce the politeness window before making the next request
        wait_if_needed(last_request_time, delay=6)

        # Download the current page
        html = fetch_page(current_url)

        # Record the request completion time after the fetch attempt
        last_request_time = time.time()

        # If fetching failed, stop the crawl gracefully
        if html is None:
            print(f"[ERROR] Crawling stopped because page {page_number} could not be fetched.")
            break

        # Parse the downloaded page into a structured record
        page_record = parse_page(html, current_url, page_number)
        crawled_pages.append(page_record)

        # Move to the next page if one exists
        current_url = find_next_page(html, current_url)
        page_number += 1

    return crawled_pages