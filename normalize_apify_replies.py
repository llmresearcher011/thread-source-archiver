import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .extract_links import extract_tco_links


def ms_to_iso(ms: Any) -> str:
    """Convert millisecond epoch timestamps to ISO-8601 UTC strings."""
    if ms in (None, ""):
        return ""
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return ""


def normalize_rows(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize provider reply rows into a clean target-link manifest."""
    output_rows: List[Dict[str, Any]] = []

    for idx, row in enumerate(rows, start=1):
        reply_text = row.get("replyText") or row.get("text") or ""
        links = extract_tco_links(reply_text)

        base = {
            "index_number": idx,
            "root_post_id": row.get("postId", ""),
            "index_reply_id": row.get("replyId", row.get("id", "")),
            "index_reply_url": row.get("replyUrl", row.get("url", "")),
            "index_reply_text": reply_text,
            "posted_at_utc": ms_to_iso(row.get("timestamp")),
            "conversation_id": row.get("conversationId", ""),
            "author_screen_name": (row.get("author") or {}).get("screenName", ""),
            "raw_json": json.dumps(row, ensure_ascii=False),
        }

        if not links:
            output_rows.append({**base, "tco_url": "", "expanded_url": "", "expand_status": "no_tco_found"})
            continue

        for link in links:
            output_rows.append({**base, "tco_url": link, "expanded_url": "", "expand_status": "pending"})

    return output_rows


def write_csv(rows: List[Dict[str, Any]], output_path: Path) -> None:
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return

    fieldnames = [
        "index_number",
        "root_post_id",
        "index_reply_id",
        "index_reply_url",
        "index_reply_text",
        "tco_url",
        "expanded_url",
        "expand_status",
        "posted_at_utc",
        "conversation_id",
        "author_screen_name",
        "raw_json",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Apify X reply export JSON into a link manifest CSV.")
    parser.add_argument("input_json", help="Path to Apify dataset JSON export.")
    parser.add_argument("--out", default="target_link_manifest.csv", help="Output CSV path.")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    output_path = Path(args.out)

    rows = json.loads(input_path.read_text(encoding="utf-8"))
    normalized = normalize_rows(rows)
    write_csv(normalized, output_path)

    print(f"Wrote {len(normalized)} rows to {output_path}")


if __name__ == "__main__":
    main()
