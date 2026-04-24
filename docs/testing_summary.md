# Testing Summary

This project uses pytest to validate crawler, indexer, search, and integration behaviour.

## Test Files

| File | Purpose |
|---|---|
| `tests/test_crawler.py` | Tests HTML parsing, pagination, request failures, crawl flow, and politeness logic |
| `tests/test_indexer.py` | Tests tokenization, index construction, document frequency, positions, and persistence |
| `tests/test_search.py` | Tests word lookup, single-word search, multi-word search, normalization, and edge cases |
| `tests/test_integration.py` | Tests build/save/load/search workflow and CLI handler behaviour |

## Running Tests

```bash
pytest tests/test_crawler.py tests/test_indexer.py tests/test_search.py tests/test_integration.py -v
```

## Coverage Areas

- parsing quote text, author, and tags  
- next-page detection  
- last-page detection  
- mocked request errors  
- politeness delay behaviour  
- lowercase tokenization  
- punctuation stripping  
- repeated terms  
- frequency statistics  
- token positions  
- JSON save/load round-trip  
- missing and invalid index files  
- single-word queries  
- multi-word query intersection  
- empty and punctuation-only queries  
- CLI handler behaviour when no index is loaded  
- CLI handler behaviour after index loading  

---

## Testing Strategy

Live network dependency is avoided in formal tests where possible. Crawler tests use mocked request behaviour and sample HTML so the test suite remains fast, deterministic, and reliable.

Manual scripts were used during development to inspect intermediate outputs, while formal pytest files provide the final evidence of correctness.