"""
search.py

Core search logic for the COMP3011 coursework search tool.

This module is responsible for:
- looking up individual words in the inverted index
- processing search queries
- returning pages that match one or more query terms
"""

from src.indexer import tokenize


def get_word_entry(index: dict, word: str) -> dict | None:
    """
    Look up a single word in the inverted index.

    The word is normalized using the same tokenizer used during indexing
    so that search remains case-insensitive and punctuation-safe.

    Parameters:
        index (dict): The inverted index.
        word (str): The word to look up.

    Returns:
        dict | None:
            The posting entry for the word if found, otherwise None.
    """
    # Tokenize the input so the lookup uses the same normalization rules
    tokens = tokenize(word)

    # If tokenization produces no valid tokens, treat the input as invalid
    if not tokens:
        return None

    # Only use the first token because this function is for single-word lookup
    normalized_word = tokens[0]

    return index.get(normalized_word)

def format_word_entry(index: dict, word: str) -> dict | None:
    """
    Return a formatted word entry for display purposes.

    Parameters:
        index (dict): The inverted index.
        word (str): The word to format.

    Returns:
        dict | None:
            A simplified display-friendly structure if the word exists,
            otherwise None.
    """
    entry = get_word_entry(index, word)

    if entry is None:
        return None

    return {
        "word": tokenize(word)[0],
        "document_frequency": entry["document_frequency"],
        "pages": entry["pages"],
    }

def get_pages_for_term(index: dict, term: str) -> set[str]:
    """
    Return the set of page URLs containing a given term.

    Parameters:
        index (dict): The inverted index.
        term (str): The term to search for.

    Returns:
        set[str]: Set of page URLs containing the term.
    """
    entry = get_word_entry(index, term)

    # If the word is not found, return an empty set
    if entry is None:
        return set()

    return set(entry["pages"].keys())


def find_query(index: dict, query: str) -> list[str]:
    """
    Search the inverted index for a query string.

    Query behaviour:
    - normalize query using the shared tokenizer
    - if one term is present, return all matching pages
    - if multiple terms are present, return only pages containing all terms

    Parameters:
        index (dict): The inverted index.
        query (str): Raw query string.

    Returns:
        list[str]: Sorted list of matching page URLs.
    """
    # Normalize the query using the same tokenizer as indexing
    query_terms = tokenize(query)

    # If the query becomes empty after normalization, return no matches
    if not query_terms:
        return []

    # Remove duplicate query terms while preserving order
    unique_terms = []
    seen_terms = set()

    for term in query_terms:
        if term not in seen_terms:
            unique_terms.append(term)
            seen_terms.add(term)

    # Get the page set for the first unique term
    matching_pages = get_pages_for_term(index, unique_terms[0])

    # Intersect with page sets for each remaining unique term
    for term in unique_terms[1:]:
        matching_pages = matching_pages.intersection(get_pages_for_term(index, term))

    # Return results in sorted order for deterministic output
    return sorted(matching_pages)