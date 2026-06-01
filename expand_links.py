import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple

import requests


def expand_url(url: str, timeout: int = 20) -> Tuple[str, str]:
    """Resolve redirects and return (expanded_url, status)."""
    if not url:
        return "", "no_url"

    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (compatible; AetherMindSourceArchiver/0.1)"},
        )
        return response.url, f"ok:{response.status_code}"
    except requests.RequestException as exc:
        return "", f"error:{type(exc).__name__}"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Expand t.co links in a target link manifest CSV.")
    parser.add_argument("input_csv", help="Path to target_link_manifest.csv.")
    parser.add_argument("--out", default="expanded_target_link_manifest.csv", help="Output CSV path.")
    args = parser.parse_args()

    rows = read_csv(Path(args.input_csv))

    for row in rows:
        tco_url = row.get("tco_url", "")
        if not tco_url:
            row["expanded_url"] = ""
            row["expand_status"] = "no_tco_found"
            continue

        expanded_url, status = expand_url(tco_url)
        row["expanded_url"] = expanded_url
        row["expand_status"] = status

    write_csv(Path(args.out), rows)
    print(f"Wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
