"""
search.py

Core search logic for the COMP3011 coursework search tool.

This module is responsible for:
- looking up individual words in the inverted index
- processing search queries
- returning pages that match one or more query terms
"""

from src.indexer import tokenize
import math


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

def get_total_documents(index: dict) -> int:
    """
    Count the total number of unique pages/documents in the index.

    This is needed for TF-IDF scoring.
    """
    all_pages = set()

    for term_data in index.values():
        all_pages.update(term_data["pages"].keys())

    return len(all_pages)

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

    ranked_pages = sorted(
        matching_pages,
        key=lambda page_url: (
            -compute_tf_idf_score(index, unique_terms, page_url),
            page_url,
        ),
    )

    return ranked_pages

def get_query_summary(results: list[str]) -> dict:
    """
    Generate a small summary for a search result set.

    Parameters:
        results (list[str]): List of matching page URLs.

    Returns:
        dict: Summary information for later CLI use.
    """
    return {
        "match_count": len(results),
        "pages": results,
    }

def compute_tf_idf_score(index: dict, query_terms: list[str], page_url: str) -> float:
    """
    Compute a simple TF-IDF relevance score for a page.

    TF-IDF combines:
    - term frequency: how often a query term appears in the page
    - inverse document frequency: how rare the term is across all pages

    Parameters:
        index (dict): The inverted index.
        query_terms (list[str]): Normalized query terms.
        page_url (str): Page URL being scored.

    Returns:
        float: TF-IDF relevance score.
    """
    total_documents = get_total_documents(index)

    if total_documents == 0:
        return 0.0

    score = 0.0

    for term in query_terms:
        if term not in index:
            continue

        term_data = index[term]
        document_frequency = term_data["document_frequency"]

        if page_url not in term_data["pages"]:
            continue

        term_frequency = term_data["pages"][page_url]["frequency"]

        # Smoothed IDF prevents division by zero and keeps scoring stable
        inverse_document_frequency = math.log((total_documents + 1) / (document_frequency + 1)) + 1

        score += term_frequency * inverse_document_frequency

    return score