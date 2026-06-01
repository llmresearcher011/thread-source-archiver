from aethermind_source_archiver.extract_links import extract_tco_links


def test_extract_tco_links():
    text = "First https://t.co/abc123 and second https://t.co/XYZ789"
    assert extract_tco_links(text) == ["https://t.co/abc123", "https://t.co/XYZ789"]


def test_extract_empty():
    assert extract_tco_links("") == []
