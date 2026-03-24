"""
crawler.py

Core crawler logic for the COMP3011 coursework search tool.

This stage focuses on:
- downloading pages from quotes.toscrape.com
- preparing functions for parsing and pagination
"""

import requests


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