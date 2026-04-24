# COMP3011 Coursework 2 — Web Crawler Search Tool

This project implements a command-line search tool for `quotes.toscrape.com`.

The application crawls the website, extracts quote content, builds an inverted index, saves the index to disk, and allows users to search the indexed pages using an interactive shell.

## Features

- Crawls paginated pages from `quotes.toscrape.com`
- Enforces a 6-second politeness delay between requests
- Extracts quote text, authors, and tags
- Builds a case-insensitive inverted index
- Stores word frequency and token position statistics
- Saves and loads the index using JSON
- Supports single-word and multi-word search
- Provides an interactive CLI shell
- Includes formal pytest coverage for crawler, indexer, search, and integration behaviour

## Requirements

- Python 3.11+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run from the project root using module mode:

```bash
python -m src.main
```

Do not run using `python src/main.py`, because the project uses package-style imports such as `src.crawler`.

---

## CLI Commands
```bash
text
build
load
print <word>
find <query>
help
exit
```

## Example Command Flow
```bash
build
print life
find life
find good friends
load
print life
find good friends
help
exit
```

## Command Descriptions

| Command | Description |
|--------|------------|
| `build` | Crawls the website, builds the inverted index, saves it to `data/index.json`, and keeps it in memory |
| `load` | Loads the saved index from `data/index.json` |
| `print <word>` | Prints the inverted index entry for a word, including frequency and positions |
| `find <query>` | Returns pages containing all query terms |
| `help` | Displays available commands |
| `exit` | Exits the shell |

---

## Search Behaviour

Search is case-insensitive.

The same tokenizer is used during both indexing and searching:
- text is lowercased  
- punctuation is removed  
- words are split on whitespace  

Multi-word queries use page-set intersection. For example:

```text
find good friends
```

returns only pages that contain both ```good``` and ```friends```.

## Index Structure

The inverted index stores each term with:

- document frequency  
- page URLs  
- per-page frequency  
- token positions  

### Example Structure

```python
{
    "life": {
        "document_frequency": 2,
        "pages": {
            "page1": {
                "frequency": 3,
                "positions": [0, 4, 8]
            }
        }
    }
}
```

## Project Structure

```text
COMP3011-cwk2/
├── data/
│   └── index.json
├── docs/
│   └── demo_checklist.md
├── src/
│   ├── __init__.py
│   ├── crawler.py
│   ├── indexer.py
│   ├── main.py
│   └── search.py
├── tests/
│   ├── __init__.py
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_search.py
│   └── test_integration.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Running Tests

Run all formal tests:

```bash
pytest tests/test_crawler.py tests/test_indexer.py tests/test_search.py tests/test_integration.py -v
```

## The Test Suite Covers

- crawler parsing and pagination  
- request failure handling  
- politeness delay logic  
- tokenization  
- inverted index construction  
- index persistence  
- search logic  
- CLI handler integration  

---

## Design Decisions

### Crawler

The crawler is split into small functions:

- `fetch_page`  
- `parse_page`  
- `find_next_page`  
- `crawl_site`  

This makes the crawler easier to test and explain.

---

### Politeness

A 6-second delay is enforced between successive requests to avoid overloading the target website.

---

### Inverted Index

The index stores frequency and position statistics to support the required `print <word>` command and future search extensions.

---

### Multi-word Query Definition

Multi-word queries return only pages that contain **all query terms**, implemented using page-set intersection.

---

### Persistence

The index is saved as JSON because it is simple, readable, and easy to inspect during testing or demonstration.

---

### Search

Multi-word search uses intersection between page sets, meaning all query terms must appear on a page for it to be returned.

---

## Edge Cases Handled

- loading before an index file exists  
- printing before an index is loaded  
- searching before an index is loaded  
- empty commands  
- invalid commands  
- missing words  
- empty queries  
- punctuation-heavy queries  
- repeated search terms  
- malformed page records  
- request timeouts and HTTP errors  

---

## GenAI Usage Declaration

Generative AI was used as a development support tool for planning, code structure suggestions, debugging guidance, and reflection. All generated suggestions were reviewed, tested, and adapted manually. 
