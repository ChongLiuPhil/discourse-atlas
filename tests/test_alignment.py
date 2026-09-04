import json
from copy import deepcopy
from pathlib import Path

from discourse_atlas.alignment import propose_alignment, validate_alignment
from discourse_atlas.evaluation import (
    compare_annotations_with_alignment,
    evaluate_against_references,
    evaluate_with_alignment,
)

ROOT = Path(__file__).resolve().parents[1]


def _doc(ids=("work", "a", "b")):
    work, a, b = ids
    anchors = [
        {"id": "x1", "paragraph_start": 1, "paragraph_end": 1, "line_start": None, "line_end": None, "section_label": None},
        {"id": "x2", "paragraph_start": 2, "paragraph_end": 2, "line_start": None, "line_end": None, "section_label": None},
        {"id": "x3", "paragraph_start": 3, "paragraph_end": 3, "line_start": None, "line_end": None, "section_label": None},
    ]
    nodes = [
        {"id": work, "parent_id": None, "kind": "work", "structure_origin": "author", "anchor_ids": ["x1", "x2", "x3"]},
        {"id": a, "parent_id": work, "kind": "section", "structure_origin": "inferred", "anchor_ids": ["x1"]},
        {"id": b, "parent_id": work, "kind": "section", "structure_origin": "inferred", "anchor_ids": ["x2", "x3"]},
    ]
    edges = [{"id": "e", "source": a, "target": b, "relation": "supports", "evidence_anchor_ids": ["x1", "x2"]}]
    return {"anchors": anchors, "nodes": nodes, "edges": edges}


def test_anchor_alignment_recovers_renamed_ids():
    reference = _doc()
    candidate = _doc(("root", "alpha", "beta"))
    alignment = propose_alignment(reference, candidate, threshold=0.5)
    assert validate_alignment(alignment, reference, candidate) == []
    report = evaluate_with_alignment(reference, candidate, alignment)
    assert report["macro_score"] == 1.0
    assert report["relation_edges"]["f1"] == 1.0


def test_split_merge_alignment_collapses_internal_candidate_edge():
    reference = _doc()
    candidate = _doc(("root", "alpha", "beta"))
    candidate["nodes"].append({"id": "beta2", "parent_id": "root", "kind": "section", "structure_origin": "inferred", "anchor_ids": ["x3"]})
    candidate["nodes"][2]["anchor_ids"] = ["x2"]
    candidate["edges"] = [
        {"id": "internal", "source": "beta", "target": "beta2", "relation": "sequence", "evidence_anchor_ids": ["x2", "x3"]},
        {"id": "e", "source": "alpha", "target": "beta", "relation": "supports", "evidence_anchor_ids": ["x1", "x2"]},
    ]
    alignment = {
        "alignment_version": "0.1.0",
        "units": [
            {"unit_id": "u0", "reference_node_ids": ["work"], "candidate_node_ids": ["root"], "status": "accepted"},
            {"unit_id": "u1", "reference_node_ids": ["a"], "candidate_node_ids": ["alpha"], "status": "accepted"},
            {"unit_id": "u2", "reference_node_ids": ["b"], "candidate_node_ids": ["beta", "beta2"], "status": "accepted"},
        ],
    }
    report = evaluate_with_alignment(reference, candidate, alignment)
    assert report["unit_coverage"]["f1"] == 1.0
    assert report["relation_edges"]["f1"] == 1.0
    assert report["node_anchors"]["f1"] == 1.0


def test_unmatched_anchorless_node_is_penalized():
    reference = _doc()
    candidate = _doc(("root", "alpha", "beta"))
    candidate["nodes"].append({"id": "orphan", "parent_id": "root", "kind": "section", "structure_origin": "inferred", "anchor_ids": []})
    report = evaluate_with_alignment(reference, candidate, propose_alignment(reference, candidate))
    assert report["unit_coverage"]["precision"] < 1.0


def test_multi_reference_reports_best_reference():
    candidate = _doc(("root", "alpha", "beta"))
    exact = deepcopy(candidate)
    worse = deepcopy(candidate)
    worse["edges"] = []
    report = evaluate_against_references([("worse", worse), ("exact", exact)], candidate)
    assert report["best_reference"] == "exact"
    assert report["best_macro_score"] == 1.0


def test_public_domain_mill_references_agree_after_reviewed_split_merge_alignment():
    case = ROOT / "benchmark" / "cases" / "mill-on-liberty"
    left = json.loads((case / "reference-a.json").read_text())
    right = json.loads((case / "reference-b.json").read_text())
    alignment = json.loads((case / "alignment-a-b.json").read_text())
    report = compare_annotations_with_alignment(left, right, alignment)
    assert report["unit_jaccard"] == 1.0
    assert report["relation_edge_jaccard"] == 1.0
    assert report["edge_evidence_jaccard"] == 1.0


def test_reviewed_alignment_matches_alignment_schema():
    from jsonschema import Draft202012Validator
    schema = json.loads((ROOT / "schemas" / "node-alignment.schema.json").read_text())
    alignment = json.loads((ROOT / "benchmark" / "cases" / "mill-on-liberty" / "alignment-a-b.json").read_text())
    assert list(Draft202012Validator(schema).iter_errors(alignment)) == []
