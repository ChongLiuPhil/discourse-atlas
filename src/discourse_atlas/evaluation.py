from __future__ import annotations

from typing import Iterable


def _prf(gold: set, candidate: set) -> dict[str, float | int]:
    true_positive = len(gold & candidate)
    precision = true_positive / len(candidate) if candidate else (1.0 if not gold else 0.0)
    recall = true_positive / len(gold) if gold else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "true_positive": true_positive,
        "gold_count": len(gold),
        "candidate_count": len(candidate),
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
    }


def _accuracy(pairs: Iterable[tuple[object, object]]) -> dict[str, float | int]:
    pairs = list(pairs)
    correct = sum(left == right for left, right in pairs)
    total = len(pairs)
    return {
        "correct": correct,
        "total": total,
        "accuracy": round(correct / total, 6) if total else 1.0,
    }


def _node_map(document: dict) -> dict[str, dict]:
    return {node["id"]: node for node in document["nodes"]}


def _edge_key(edge: dict) -> tuple[str, str, str]:
    source, target, relation = edge["source"], edge["target"], edge["relation"]
    if relation == "contrasts":
        source, target = sorted((source, target))
    return source, target, relation


def _edge_signatures(document: dict) -> set[tuple[str, str, str]]:
    return {_edge_key(edge) for edge in document["edges"]}


def _node_anchor_signatures(document: dict) -> set[tuple[str, str]]:
    return {
        (node["id"], anchor_id)
        for node in document["nodes"]
        for anchor_id in node.get("anchor_ids", [])
    }


def _edge_evidence_signatures(document: dict) -> set[tuple[str, str, str, str]]:
    result = set()
    for edge in document["edges"]:
        source, target, relation = _edge_key(edge)
        for anchor_id in edge.get("evidence_anchor_ids", []):
            result.add((source, target, relation, anchor_id))
    return result


def evaluate_documents(gold: dict, candidate: dict) -> dict:
    """Evaluate a candidate against a benchmark graph with stable node IDs.

    This intentionally avoids fuzzy semantic node alignment. Benchmark cases should
    publish stable IDs, or an alignment should be performed before calling this
    function. That keeps the metric inspectable rather than hiding matching errors
    inside an embedding/model heuristic.
    """

    gold_nodes = _node_map(gold)
    candidate_nodes = _node_map(candidate)
    shared_ids = set(gold_nodes) & set(candidate_nodes)
    non_root_shared = {
        node_id
        for node_id in shared_ids
        if gold_nodes[node_id].get("parent_id") is not None
    }

    result = {
        "node_id_coverage": _prf(set(gold_nodes), set(candidate_nodes)),
        "hierarchy_parent_accuracy": _accuracy(
            (gold_nodes[node_id].get("parent_id"), candidate_nodes[node_id].get("parent_id"))
            for node_id in sorted(non_root_shared)
        ),
        "structure_origin_accuracy": _accuracy(
            (gold_nodes[node_id].get("structure_origin"), candidate_nodes[node_id].get("structure_origin"))
            for node_id in sorted(shared_ids)
        ),
        "relation_edges": _prf(_edge_signatures(gold), _edge_signatures(candidate)),
        "node_anchors": _prf(_node_anchor_signatures(gold), _node_anchor_signatures(candidate)),
        "edge_evidence": _prf(
            _edge_evidence_signatures(gold),
            _edge_evidence_signatures(candidate),
        ),
    }

    components = [
        result["node_id_coverage"]["f1"],
        result["hierarchy_parent_accuracy"]["accuracy"],
        result["structure_origin_accuracy"]["accuracy"],
        result["relation_edges"]["f1"],
        result["node_anchors"]["f1"],
        result["edge_evidence"]["f1"],
    ]
    result["macro_score"] = round(sum(components) / len(components), 6)
    return result


def compare_annotations(left: dict, right: dict) -> dict:
    """Symmetric agreement summary for two human/AI reconstructions with aligned IDs."""
    left_nodes = _node_map(left)
    right_nodes = _node_map(right)
    shared_ids = set(left_nodes) & set(right_nodes)
    non_root_shared = {
        node_id for node_id in shared_ids
        if left_nodes[node_id].get("parent_id") is not None
        and right_nodes[node_id].get("parent_id") is not None
    }

    def jaccard(a: set, b: set) -> float:
        union = a | b
        return round(len(a & b) / len(union), 6) if union else 1.0

    return {
        "shared_node_ids": len(shared_ids),
        "node_id_jaccard": jaccard(set(left_nodes), set(right_nodes)),
        "hierarchy_parent_agreement": _accuracy(
            (left_nodes[node_id].get("parent_id"), right_nodes[node_id].get("parent_id"))
            for node_id in sorted(non_root_shared)
        ),
        "structure_origin_agreement": _accuracy(
            (left_nodes[node_id].get("structure_origin"), right_nodes[node_id].get("structure_origin"))
            for node_id in sorted(shared_ids)
        ),
        "relation_edge_jaccard": jaccard(_edge_signatures(left), _edge_signatures(right)),
        "node_anchor_jaccard": jaccard(_node_anchor_signatures(left), _node_anchor_signatures(right)),
        "edge_evidence_jaccard": jaccard(
            _edge_evidence_signatures(left), _edge_evidence_signatures(right)
        ),
    }
