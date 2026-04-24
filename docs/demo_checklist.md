# Demo Checklist

## Start command

```
python -m src.main
```

## Core Command Flow
- build  
- print life  
- find life  
- find good friends  
- load  
- print life  
- find good friends  
- help  
- exit  

## Edge Cases to Show

- print unknownword  
- find unknownword  
- invalid command: hello  
- empty query: find  
- print before load/build in a fresh session  

## Points to Explain

- The crawler follows pagination from quotes.toscrape.com  
- The crawler enforces a 6-second politeness delay  
- The index stores frequency and token positions  
- Multi-word search uses page-set intersection  
- The index is saved and loaded from `data/index.json`  
- Tests are split into crawler, indexer, search, and integration tests  