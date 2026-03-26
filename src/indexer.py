"""
indexer.py

Core indexing logic for the COMP3011 coursework search tool.

This module is responsible for:
- tokenizing page content
- building an inverted index
- storing frequency and position information for each term
"""

import re


def tokenize(text: str) -> list[str]:
    """
    Convert raw text into a normalized list of tokens.

    Tokenization rules:
    - convert to lowercase
    - remove punctuation
    - split into words

    Parameters:
        text (str): Raw text to tokenize.

    Returns:
        list[str]: List of normalized tokens.
    """
    # Convert the text to lowercase so search becomes case-insensitive
    normalized_text = text.lower()

    # Replace any non-alphanumeric characters with spaces
    # This removes punctuation while keeping letters and numbers
    normalized_text = re.sub(r"[^a-z0-9]+", " ", normalized_text)

    # Split the cleaned text into tokens and remove any empty strings
    tokens = normalized_text.split()

    return tokens


def create_term_entry() -> dict:
    """
    Create the default structure for a new term in the inverted index.

    Returns:
        dict: Empty term entry with document frequency and page postings.
    """
    return {
        "document_frequency": 0,
        "pages": {},
    }


def build_index(crawled_pages: list[dict]) -> dict:
    """
    Build an inverted index from a list of crawled page records.

    Each page record is expected to include:
    - url
    - content

    The index stores:
    - document frequency for each term
    - per-page frequency for each term
    - token positions within each page

    Parameters:
        crawled_pages (list[dict]): List of page records from the crawler.

    Returns:
        dict: Inverted index mapping terms to posting information.
    """
    index = {}

    # Process each crawled page one at a time
    for page in crawled_pages:
        page_url = page.get("url")
        page_content = page.get("content", "")

        # Skip malformed page records that do not have a valid URL
        if not page_url:
            continue

        # Tokenize the page content into normalized words
        tokens = tokenize(page_content)

        # Track which terms have already appeared in this page
        # so document_frequency only increases once per page
        terms_seen_in_page = set()

        # Enumerate tokens so we can store positions
        for position, token in enumerate(tokens):
            # Create a new entry if this term has not appeared before
            if token not in index:
                index[token] = create_term_entry()

            # Create a page-level posting if this term has not appeared
            # in the current page before
            if page_url not in index[token]["pages"]:
                index[token]["pages"][page_url] = {
                    "frequency": 0,
                    "positions": [],
                }

            # Increase the frequency count for this term in the current page
            index[token]["pages"][page_url]["frequency"] += 1

            # Store the token position within the current page
            index[token]["pages"][page_url]["positions"].append(position)

            # Increase document frequency only once per page
            if token not in terms_seen_in_page:
                index[token]["document_frequency"] += 1
                terms_seen_in_page.add(token)

    return index