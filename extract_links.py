import re
from typing import List

TCO_RE = re.compile(r"https://t\.co/[A-Za-z0-9]+")


def extract_tco_links(text: str) -> List[str]:
    """Return all t.co links found in text."""
    if not text:
        return []
    return TCO_RE.findall(text)
