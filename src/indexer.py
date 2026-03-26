"""
indexer.py

Core indexing logic for the COMP3011 coursework search tool.

This module is responsible for:
- tokenizing page content
- building an inverted index
- storing frequency and position information for each term
"""

import re

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