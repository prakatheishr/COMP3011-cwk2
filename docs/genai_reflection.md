# GenAI Critical Evaluation

## Overview

Generative AI was used throughout this project as a development support tool for planning, structuring, debugging, and testing.

All outputs were critically reviewed and adapted before inclusion in the final implementation.

---

## Where GenAI Helped

### 1. Planning the System

- Broke the coursework into stages (crawler → indexer → search → CLI → tests)
- Suggested a feature-branch workflow
- Helped structure incremental development

---

### 2. Code Structure

- Suggested modular function design (crawler, indexer, search separation)
- Helped organise CLI handlers
- Encouraged separation of concerns for testing

---

### 3. Debugging

Examples:
- Fixing import issues (`python -m src.main`)
- Resolving test failures after output changes
- Improving edge-case handling

---

### 4. Testing

- Suggested pytest structure
- Identified important test cases (multi-word queries, missing terms)
- Helped design integration tests

---

## Where GenAI Was Wrong / Limited

### 1. Overcomplicated solutions

- Some suggestions added unnecessary abstraction
- Required simplification to match coursework scope

---

### 2. Incorrect assumptions

- Occasionally misunderstood project structure (e.g., imports)
- Suggested implementations that didn’t match the brief exactly

---

### 3. Missed edge cases

Examples:
- CLI output formatting breaking tests
- Some validation cases not initially covered

---

## What I Changed

- Simplified data structures for clarity
- Adjusted CLI output for usability and testing
- Refined tests to match actual behaviour
- Removed unnecessary complexity

---

## What I Learned

- Importance of validating AI-generated code
- How inverted indexes work in practice
- How to design testable, modular systems
- How to handle edge cases in CLI tools

---

## Impact on Development

GenAI:
- sped up planning and structuring
- helped debug faster
- improved test coverage ideas

However:
- required constant verification
- sometimes slowed debugging when incorrect suggestions were followed

---

## Conclusion

GenAI was a useful assistant for planning, debugging, and structuring, but not a replacement for understanding. The final implementation reflects manual refinement and validation of all generated outputs.