"""
crawler.py

Core crawler logic for the COMP3011 coursework search tool.

This stage focuses on:
- downloading pages from quotes.toscrape.com
- extracting quote content from each page
- following pagination links
"""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch_page(url: str) -> str:
    """
    Download a page and return its HTML content.

    Parameters:
        url (str): The URL to fetch.

    Returns:
        str: Raw HTML content of the page.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


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