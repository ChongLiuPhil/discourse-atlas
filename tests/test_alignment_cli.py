import json
from pathlib import Path

from discourse_atlas.cli import main

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "benchmark" / "cases" / "mill-on-liberty"


def test_alignment_cli_scores_reviewed_split_merge_as_one(tmp_path, capsys):
    proposed = tmp_path / "proposed.json"
    assert main(["align", str(CASE / "reference-a.json"), str(CASE / "reference-b.json"), "-o", str(proposed)]) == 0
    assert proposed.exists()
    assert main([
        "evaluate",
        str(CASE / "reference-a.json"),
        str(CASE / "reference-b.json"),
        "--alignment",
        str(CASE / "alignment-a-b.json"),
    ]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["evaluation_mode"] == "explicit-unit-alignment"
    assert report["macro_score"] == 1.0


def test_multi_evaluate_keeps_reference_distribution(capsys):
    assert main([
        "multi-evaluate",
        str(CASE / "reference-b.json"),
        str(CASE / "reference-a.json"),
        str(CASE / "reference-b.json"),
        "--auto-align",
    ]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["reference_count"] == 2
    assert report["best_reference"].endswith("reference-b.json")
    assert report["best_macro_score"] == 1.0
