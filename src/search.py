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