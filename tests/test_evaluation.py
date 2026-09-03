import json
from pathlib import Path

from discourse_atlas.evaluation import compare_annotations, evaluate_documents

ROOT = Path(__file__).resolve().parents[1]


def load_example():
    return json.loads((ROOT / "examples" / "mini-essay" / "analysis.json").read_text())


def test_identical_document_scores_one():
    doc = load_example()
    report = evaluate_documents(doc, doc)
    assert report["macro_score"] == 1.0
    assert report["relation_edges"]["f1"] == 1.0
    assert report["edge_evidence"]["f1"] == 1.0


def test_missing_relation_reduces_recall():
    gold = load_example()
    candidate = load_example()
    candidate["edges"] = candidate["edges"][:-1]
    report = evaluate_documents(gold, candidate)
    assert report["relation_edges"]["precision"] == 1.0
    assert report["relation_edges"]["recall"] < 1.0


def test_agreement_is_symmetric_for_edge_jaccard():
    left = load_example(); right = load_example(); right["edges"] = right["edges"][:-1]
    assert compare_annotations(left, right)["relation_edge_jaccard"] == compare_annotations(right, left)["relation_edge_jaccard"]


def test_contrast_is_scored_symmetrically():
    left = load_example(); right = load_example()
    contrast = {"id":"contrast-test","source":"sec-1","target":"sec-2","relation":"contrasts","explanation":"Test contrast","evidence_anchor_ids":["a-p1","a-p2"],"confidence":0.8,"assertion_level":"tentative","notes":None}
    left["edges"]=[contrast]; right["edges"]=[{**contrast,"source":"sec-2","target":"sec-1"}]
    assert evaluate_documents(left, right)["relation_edges"]["f1"] == 1.0


def test_all_manifest_gold_cases_validate_and_self_score():
    from discourse_atlas.cli import validate_document
    manifest = json.loads((ROOT / "benchmark" / "manifest.json").read_text())
    assert len(manifest["cases"]) >= 4
    for case in manifest["cases"]:
        gold = json.loads((ROOT / case["gold"]).read_text())
        assert validate_document(gold) == []
        assert evaluate_documents(gold, gold)["macro_score"] == 1.0
