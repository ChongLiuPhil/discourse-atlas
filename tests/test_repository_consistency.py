import json
from pathlib import Path

import pytest

from discourse_atlas.cli import validate_document

ROOT = Path(__file__).resolve().parents[1]
GRAPH_FIXTURES = [
    "examples/mini-essay/analysis.json",
    "skills/discourse-structure/examples/mini-essay.analysis.json",
    "benchmark/annotations/mini-essay-a.json",
    "benchmark/annotations/mini-essay-b.json",
    "benchmark/cases/academic-mechanism/gold.json",
    "benchmark/cases/mill-on-liberty/reference-a.json",
    "benchmark/cases/mill-on-liberty/reference-b.json",
    "benchmark/cases/mini-essay/gold.json",
    "benchmark/cases/philosophy-counterexample/gold.json",
    "benchmark/cases/policy-library/gold.json",
]


@pytest.mark.parametrize("relative_path", GRAPH_FIXTURES)
def test_maintained_graph_fixtures_validate_against_current_schema(relative_path):
    document = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
    assert document["schema_version"] == "0.2.0"
    assert validate_document(document) == []
