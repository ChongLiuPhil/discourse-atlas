import json
from pathlib import Path

from discourse_atlas.cli import to_dot, to_mermaid, validate_document


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "mini-essay" / "analysis.json"


def load_example():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_is_valid():
    assert validate_document(load_example()) == []


def test_packaged_schema_matches_repository_schema():
    repository_schema = ROOT / "schemas" / "discourse-graph.schema.json"
    versioned_schema = ROOT / "schemas" / "discourse-graph" / "0.2.0.schema.json"
    packaged_schema = ROOT / "src" / "discourse_atlas" / "resources" / "discourse-graph.schema.json"
    assert repository_schema.read_text(encoding="utf-8") == versioned_schema.read_text(encoding="utf-8")
    assert repository_schema.read_text(encoding="utf-8") == packaged_schema.read_text(encoding="utf-8")


def test_legacy_schema_profile_matches_packaged_resource():
    repository_schema = ROOT / "schemas" / "discourse-graph" / "0.1.0-legacy.schema.json"
    packaged_schema = ROOT / "src" / "discourse_atlas" / "resources" / "discourse-graph-0.1.0-legacy.schema.json"
    assert repository_schema.read_text(encoding="utf-8") == packaged_schema.read_text(encoding="utf-8")


def test_example_uses_current_graph_schema_version():
    assert load_example()["schema_version"] == "0.2.0"


def test_legacy_0_1_compatibility_profile_is_supported():
    doc = load_example()
    doc["schema_version"] = "0.1.0"
    assert validate_document(doc) == []


def test_unknown_schema_version_is_rejected():
    doc = load_example()
    doc["schema_version"] = "9.9.9"
    errors = validate_document(doc)
    assert any("unsupported or missing version" in error for error in errors)


def test_main_claim_is_optional_but_must_be_nonempty_when_present():
    doc = load_example()
    assert validate_document(doc) == []

    legacy = load_example()
    legacy["nodes"][0].pop("main_claim")
    assert validate_document(legacy) == []

    invalid = load_example()
    invalid["nodes"][0]["main_claim"] = ""
    assert validate_document(invalid)


def test_zero_install_protocol_points_to_canonical_resources():
    protocol = (ROOT / "AGENT.md").read_text(encoding="utf-8")
    assert "https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/AGENT.md" in protocol
    assert "https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/schemas/discourse-graph.schema.json" in protocol
    assert "main_claim" in protocol
    assert "Do not require the user to install Discourse Atlas" in protocol


def test_mermaid_contains_edges_and_groups():
    output = to_mermaid(load_example())
    assert "flowchart TB" in output
    assert 'sec-2 -->|"requires"| sec-3' in output
    assert 'subgraph work["Why Definitions Matter in Disagreement"]' in output


def test_dot_contains_cluster_and_edge():
    output = to_dot(load_example())
    assert 'subgraph "cluster_work"' in output
    assert '"sec-2" -> "sec-3" [label="requires"]' in output


def test_invalid_relation_is_rejected():
    doc = load_example()
    doc["edges"][0]["relation"] = "causes"
    assert validate_document(doc)


def test_unknown_edge_endpoint_is_rejected():
    doc = load_example()
    doc["edges"][0]["target"] = "missing-node"
    assert any("unknown target node missing-node" in e for e in validate_document(doc))


def test_unknown_anchor_reference_is_rejected():
    doc = load_example()
    doc["nodes"][1]["anchor_ids"] = ["missing-anchor"]
    assert "node sec-1: unknown anchor_id missing-anchor" in validate_document(doc)


def test_duplicate_ids_are_rejected():
    doc = load_example()
    doc["nodes"][1]["id"] = "work"
    assert "duplicate node id: work" in validate_document(doc)


def test_containment_cycle_is_rejected():
    doc = load_example()
    doc["nodes"][0]["parent_id"] = "sec-1"
    assert any("containment cycle detected" in e for e in validate_document(doc))


def test_invalid_anchor_range_is_rejected():
    doc = load_example()
    doc["anchors"][0]["paragraph_start"] = 3
    doc["anchors"][0]["paragraph_end"] = 1
    assert "anchor a-p1: paragraph_start must be <= paragraph_end" in validate_document(doc)
