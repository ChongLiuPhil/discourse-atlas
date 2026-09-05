import json
from pathlib import Path

from discourse_atlas.alignment import propose_alignment
from discourse_atlas.cli import validate_document

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "mini-essay" / "analysis.json"


def load_example():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_schema_accepts_page_and_character_coordinates():
    doc = load_example()
    doc["anchors"][0].update({"page_start": 12, "page_end": 13, "char_start": 40, "char_end": 96})
    assert validate_document(doc) == []


def test_invalid_scholarly_ranges_are_rejected():
    doc = load_example()
    doc["anchors"][0].update({"page_start": 9, "page_end": 8})
    assert "anchor a-p1: page_start must be <= page_end" in validate_document(doc)

    doc = load_example()
    doc["anchors"][0].update({"char_start": 20, "char_end": 20})
    assert "anchor a-p1: char_start must be < char_end" in validate_document(doc)


def test_end_coordinate_requires_start_coordinate():
    doc = load_example()
    doc["anchors"][0]["char_end"] = 12
    assert "anchor a-p1: char_end requires char_start" in validate_document(doc)


def _minimal_doc(root_id, child_id, anchor):
    return {
        "anchors": [anchor],
        "nodes": [
            {"id": root_id, "parent_id": None, "kind": "work", "anchor_ids": []},
            {"id": child_id, "parent_id": root_id, "kind": "section", "anchor_ids": [anchor["id"]]},
        ],
        "edges": [],
    }


def test_character_span_fallback_aligns_renamed_nodes():
    reference = _minimal_doc("work", "section", {"id": "a", "char_start": 64, "char_end": 160})
    candidate = _minimal_doc("root", "renamed", {"id": "b", "char_start": 64, "char_end": 160})
    alignment = propose_alignment(reference, candidate)
    assert any(unit["reference_node_ids"] == ["section"] and unit["candidate_node_ids"] == ["renamed"] for unit in alignment["units"])


def test_page_fallback_aligns_when_finer_coordinates_are_absent():
    reference = _minimal_doc("work", "section", {"id": "a", "page_start": 4, "page_end": 5})
    candidate = _minimal_doc("root", "renamed", {"id": "b", "page_start": 4, "page_end": 5})
    alignment = propose_alignment(reference, candidate)
    assert any(unit["reference_node_ids"] == ["section"] and unit["candidate_node_ids"] == ["renamed"] for unit in alignment["units"])


def test_paragraph_coordinates_take_priority_over_conflicting_character_offsets():
    reference = _minimal_doc("work", "section", {"id": "a", "paragraph_start": 2, "paragraph_end": 2, "char_start": 0, "char_end": 32})
    candidate = _minimal_doc("root", "renamed", {"id": "b", "paragraph_start": 2, "paragraph_end": 2, "char_start": 1000, "char_end": 1032})
    alignment = propose_alignment(reference, candidate)
    assert any(unit["reference_node_ids"] == ["section"] and unit["candidate_node_ids"] == ["renamed"] for unit in alignment["units"])
