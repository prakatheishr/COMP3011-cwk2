"""
main.py

Interactive command-line shell for the COMP3011 coursework search tool.

This module is responsible for:
- running the CLI loop
- connecting crawler, indexer, persistence, and search logic
- handling user commands such as build, load, print, find, and exit
"""

from src.crawler import crawl_site
from src.indexer import build_index, get_index_summary, load_index, save_index
from src.search import find_query, format_word_entry, get_query_summary

# Starting page for the crawler
START_URL = "https://quotes.toscrape.com/"

# Default path used to store the saved index
INDEX_FILEPATH = "data/index.json"

def print_success(message):
    print(f"[SUCCESS] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

index = None

def handle_build() -> dict | None:
    """
    Build the inverted index from the live website.

    This command:
    - crawls the quotes website
    - builds the inverted index
    - saves the index to disk
    - returns the index for in-memory use

    Returns:
        dict | None:
            The built index if successful, otherwise None.
    """
    print_info("Building index from live website...")

    # Crawl the target site
    pages = crawl_site(START_URL)

    if not pages:
        print_error("No pages were crawled. Index build failed.")
        return None

    # Build the inverted index from crawled page content
    index = build_index(pages)

    # Save the index to disk for later loading
    save_index(index, INDEX_FILEPATH)

    # Generate summary information for user feedback
    summary = get_index_summary(index)

    print_success(
        f"Index built successfully: {len(pages)} pages crawled, "
        f"{summary['unique_terms']} unique terms saved to {INDEX_FILEPATH}"
    )

    return index

def handle_load() -> dict | None:
    """
    Load the saved inverted index from disk.
    """
    print_info(f"Loading index from {INDEX_FILEPATH}...")

    index = load_index(INDEX_FILEPATH)

    if index is None:
        print_error("No saved index found. Run 'build' first.")
        return None

    summary = get_index_summary(index)

    print_success(
        f"Index loaded successfully from {INDEX_FILEPATH} "
        f"with {summary['unique_terms']} unique terms"
    )

    return index

def handle_print(index: dict | None, word: str) -> None:
    """
    Print the inverted index entry for a given word.
    """
    if not ensure_index_loaded(index):
        return

    # Normalize input
    word = word.strip()

    if not word:
        print_error("Please provide a valid word.")
        return

    word_entry = format_word_entry(index, word)

    if word_entry is None:
        print_error(f"Word not found in index: {word}")
        return

    print_info(
        f"Word '{word_entry['word']}' found in "
        f"{word_entry['document_frequency']} page(s)"
    )
    print(word_entry)

def handle_find(index: dict | None, query: str) -> None:
    """
    Search the index for a query and print matching pages.
    """
    if not ensure_index_loaded(index):
        return

    query = query.strip()

    if not query:
        print_error("Query cannot be empty.")
        return

    results = find_query(index, query)

    if not results:
        print_error(f"No results found for query: {query}")
        return

    summary = get_query_summary(results)

    print_info(f"Query '{query}' matched {summary['match_count']} page(s)")
    display_search_results(summary["pages"])

def ensure_index_loaded(index: dict | None) -> bool:
    """
    Check whether an index is currently loaded in memory.

    Parameters:
        index (dict | None): The current in-memory index.

    Returns:
        bool: True if an index is available, otherwise False.
    """
    if index is None:
        print_error("No index loaded. Run 'build' or 'load' first.")
        return False

    return True

def display_search_results(results: list[str]) -> None:
    """
    Print matching search result pages line by line.

    Parameters:
        results (list[str]): List of matching page URLs.
    """
    for page in results:
        print(page)

def run_shell() -> None:
    """
    Run the interactive command-line shell.
    """
    # Keep the currently loaded index in memory across commands
    index = None

    print_info("COMP3011 Search Tool")
    print_info("Available commands: build, load, print <word>, find <query>, exit")

    while True:
        command = input("> ").strip()

        # Ignore empty input
        if not command:
            continue

        if command == "exit":
            print_info("Exiting search tool...")
            break

        if command == "build":
            index = handle_build()
            continue

        if command == "load":
            index = handle_load()
            continue

        if command.startswith("print "):
            word = command[6:].strip()
            if not word:
                print_error("Please provide a word to print.")
                continue
            handle_print(index, word)
            continue

        if command.startswith("find "):
            query = command[5:].strip()
            if not query:
                print_error("Query cannot be empty.")
                continue
            handle_find(index, query)
            continue

        print_error("Invalid command.")

if __name__ == "__main__":
    run_shell()