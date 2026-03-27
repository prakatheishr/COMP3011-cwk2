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

    Returns:
        dict | None:
            The loaded index if successful, otherwise None.
    """
    print_info(f"Loading index from {INDEX_FILEPATH}...")

    index = load_index(INDEX_FILEPATH)

    if index is None:
        print_error("Index could not be loaded.")
        return None

    print_success(f"Index loaded successfully from {INDEX_FILEPATH}")
    return index


def run_shell():
    while True:
        command = input("> ").strip()
        
        if not command:
            continue

        if command == "exit":
            print_info("Exiting...")
            break

        elif command == "build":
            print_info("Building index...")
            # index = build_index(...)
            index = {}  # placeholder
            print_success("Index built")

        elif command == "load":
            print_info("Loading index...")
            index = {}  # placeholder
            print_success("Index loaded")

        elif command.startswith("print "):
            word = command[6:].strip()
            if not word:
                print_error("Please provide a word to print")
                continue

        elif command.startswith("find "):
            query = command[5:].strip()
            if not query:
                print_error("Query cannot be empty")
                continue

        else:
            print_error("Invalid command")


if __name__ == "__main__":
    run_shell()