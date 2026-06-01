# AetherMind Source Archiver

Open-source Python toolkit for turning public research-link threads into structured, AI-ready archives.

AetherMind Source Archiver is designed for builders who collect public posts, threads, links, and research references, then need to normalize them into clean datasets for downstream AI workflows such as retrieval-augmented generation, evidence packaging, and multi-model analysis.

## What this project does

1. Read exported reply/thread datasets from providers such as Apify.
2. Extract `t.co` links from public index posts.
3. Expand shortened links into destination URLs.
4. Normalize reply/thread records into a clean manifest.
5. Prepare data for storage in PostgreSQL or spreadsheet review.

## What this project does not do

This project does not require or store X/Twitter login credentials, passwords, session cookies, `auth_token`, `ct0`, or browser sessions.

It is intended for public/source-grounded research workflows and should be used only with data the user is allowed to process.

## Quick start

```bash
git clone https://github.com/YOUR_USERNAME/aethermind-source-archiver.git
cd aethermind-source-archiver

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the sample normalizer:

```bash
python -m aethermind_source_archiver.normalize_apify_replies examples/sample_apify_replies.json --out target_link_manifest.csv
```

Expand links:

```bash
python -m aethermind_source_archiver.expand_links target_link_manifest.csv --out expanded_target_link_manifest.csv
```

## Example output columns

| Column | Meaning |
|---|---|
| index_number | Row order in the source export |
| root_post_id | Root/source thread post ID |
| index_reply_id | Reply/index post ID |
| index_reply_url | URL for the index post |
| index_reply_text | Raw text from the index post |
| tco_url | Extracted shortened link |
| expanded_url | Destination URL after redirect expansion |
| expand_status | Status of link expansion |
| posted_at_utc | Timestamp converted to UTC |
| conversation_id | Source conversation/thread ID |
| author_screen_name | Source author handle |

## Roadmap

- [ ] PostgreSQL insert command
- [ ] pgvector-ready evidence chunks
- [ ] Markdown report export
- [ ] YouTube transcript connector
- [ ] Public website/RSS connector
- [ ] Link quality checks
- [ ] Media metadata extraction
- [ ] Test coverage for provider-specific JSON shapes

## License

MIT
