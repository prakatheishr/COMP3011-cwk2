"""
Manual test for index persistence.
"""

from src.crawler import crawl_site
from src.indexer import build_index, save_index, load_index


def main():
    # Crawl and build index
    pages = crawl_site("https://quotes.toscrape.com/")
    index = build_index(pages)

    # Save index
    filepath = "data/index.json"
    save_index(index, filepath)
    print("[INFO] Index saved")

    # Load index
    loaded_index = load_index(filepath)

    if loaded_index is None:
        print("[ERROR] Failed to load index")
        return

    print(f"[INFO] Loaded index contains {len(loaded_index)} terms")

    # Check equality
    if loaded_index == index:
        print("[SUCCESS] Index matches after reload")
    else:
        print("[ERROR] Index mismatch after reload")


if __name__ == "__main__":
    main()