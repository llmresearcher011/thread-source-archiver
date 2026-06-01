# Architecture

The first open-source layer is intentionally small:

```text
Provider export JSON
        ↓
Normalize provider fields
        ↓
Extract shortened links
        ↓
Expand redirects
        ↓
Write manifest CSV
        ↓
PostgreSQL / Excel / RAG pipeline later
```

## Core modules

- `extract_links.py`: finds shortened links in text
- `normalize_apify_replies.py`: maps provider JSON to a clean manifest
- `expand_links.py`: resolves redirects and writes expanded URLs

## Future private/proprietary layers

This open-source repository does not include proprietary scoring, private customer data, expert-review workflows, or commercial report templates.
