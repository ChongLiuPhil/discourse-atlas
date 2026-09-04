from __future__ import annotations

from statistics import mean
from typing import Iterable

from .alignment import (
    build_unit_maps,
    collapse_nodes,
    collapsed_edge_evidence_signatures,
    collapsed_edge_signatures,
)


def _prf(gold: set, candidate: set) -> dict[str, float | int]:
    true_positive = len(gold & candidate)
    precision = true_positive / len(candidate) if candidate else (1.0 if not gold else 0.0)
    recall = true_positive / len(gold) if gold else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"true_positive": true_positive, "gold_count": len(gold), "candidate_count": len(candidate), "precision": round(precision, 6), "recall": round(recall, 6), "f1": round(f1, 6)}


def _accuracy(pairs: Iterable[tuple[object, object]]) -> dict[str, float | int]:
    pairs = list(pairs)
    correct = sum(left == right for left, right in pairs)
    total = len(pairs)
    return {"correct": correct, "total": total, "accuracy": round(correct / total, 6) if total else 1.0}


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
    return {(node["id"], aid) for node in document["nodes"] for aid in node.get("anchor_ids", [])}


def _edge_evidence_signatures(document: dict) -> set[tuple[str, str, str, str]]:
    result = set()
    for edge in document["edges"]:
        source, target, relation = _edge_key(edge)
        for aid in edge.get("evidence_anchor_ids", []):
            result.add((source, target, relation, aid))
    return result


def _macro(result: dict) -> float:
    components = [
        result["unit_coverage"]["f1"],
        result["hierarchy_parent_accuracy"]["accuracy"],
        result["structure_origin_accuracy"]["accuracy"],
        result["relation_edges"]["f1"],
        result["node_anchors"]["f1"],
        result["edge_evidence"]["f1"],
    ]
    return round(sum(components) / len(components), 6)


def evaluate_documents(gold: dict, candidate: dict) -> dict:
    gold_nodes = _node_map(gold)
    candidate_nodes = _node_map(candidate)
    shared_ids = set(gold_nodes) & set(candidate_nodes)
    non_root_shared = {nid for nid in shared_ids if gold_nodes[nid].get("parent_id") is not None}
    result = {
        "node_id_coverage": _prf(set(gold_nodes), set(candidate_nodes)),
        "hierarchy_parent_accuracy": _accuracy((gold_nodes[nid].get("parent_id"), candidate_nodes[nid].get("parent_id")) for nid in sorted(non_root_shared)),
        "structure_origin_accuracy": _accuracy((gold_nodes[nid].get("structure_origin"), candidate_nodes[nid].get("structure_origin")) for nid in sorted(shared_ids)),
        "relation_edges": _prf(_edge_signatures(gold), _edge_signatures(candidate)),
        "node_anchors": _prf(_node_anchor_signatures(gold), _node_anchor_signatures(candidate)),
        "edge_evidence": _prf(_edge_evidence_signatures(gold), _edge_evidence_signatures(candidate)),
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
    result["evaluation_mode"] = "stable-node-id"
    return result


def evaluate_with_alignment(reference: dict, candidate: dict, alignment: dict) -> dict:
    ref_map, cand_map = build_unit_maps(reference, candidate, alignment)
    ref_units = collapse_nodes(reference, ref_map)
    cand_units = collapse_nodes(candidate, cand_map)
    shared = set(ref_units) & set(cand_units)
    non_root_shared = {uid for uid in shared if ref_units[uid]["parent_id"] is not None}
    ref_anchor_sigs = {(uid, token) for uid, unit in ref_units.items() for token in unit["anchor_tokens"]}
    cand_anchor_sigs = {(uid, token) for uid, unit in cand_units.items() for token in unit["anchor_tokens"]}
    result = {
        "unit_coverage": _prf(set(ref_units), set(cand_units)),
        "hierarchy_parent_accuracy": _accuracy((ref_units[uid]["parent_id"], cand_units[uid]["parent_id"]) for uid in sorted(non_root_shared)),
        "structure_origin_accuracy": _accuracy((ref_units[uid]["structure_origin"], cand_units[uid]["structure_origin"]) for uid in sorted(shared)),
        "relation_edges": _prf(collapsed_edge_signatures(reference, ref_map), collapsed_edge_signatures(candidate, cand_map)),
        "node_anchors": _prf(ref_anchor_sigs, cand_anchor_sigs),
        "edge_evidence": _prf(collapsed_edge_evidence_signatures(reference, ref_map), collapsed_edge_evidence_signatures(candidate, cand_map)),
        "alignment_units": len(alignment.get("units", [])),
        "evaluation_mode": "explicit-unit-alignment",
    }
    result["macro_score"] = _macro(result)
    return result


def evaluate_against_references(references: list[tuple[str, dict]], candidate: dict, alignments: dict[str, dict] | None = None) -> dict:
    reports = []
    alignments = alignments or {}
    for label, reference in references:
        if label in alignments:
            report = evaluate_with_alignment(reference, candidate, alignments[label])
        else:
            report = evaluate_documents(reference, candidate)
        reports.append({"reference": label, "macro_score": report["macro_score"], "report": report})
    if not reports:
        raise ValueError("at least one reference is required")
    scores = [item["macro_score"] for item in reports]
    best = max(reports, key=lambda item: item["macro_score"])
    return {
        "best_reference": best["reference"],
        "best_macro_score": best["macro_score"],
        "mean_macro_score": round(mean(scores), 6),
        "min_macro_score": min(scores),
        "max_macro_score": max(scores),
        "reference_count": len(reports),
        "per_reference": reports,
    }


def compare_annotations(left: dict, right: dict) -> dict:
    left_nodes = _node_map(left)
    right_nodes = _node_map(right)
    shared = set(left_nodes) & set(right_nodes)
    non_root = {nid for nid in shared if left_nodes[nid].get("parent_id") is not None and right_nodes[nid].get("parent_id") is not None}

    def jaccard(a: set, b: set) -> float:
        union = a | b
        return round(len(a & b) / len(union), 6) if union else 1.0

    return {
        "shared_node_ids": len(shared),
        "node_id_jaccard": jaccard(set(left_nodes), set(right_nodes)),
        "hierarchy_parent_agreement": _accuracy((left_nodes[nid].get("parent_id"), right_nodes[nid].get("parent_id")) for nid in sorted(non_root)),
        "structure_origin_agreement": _accuracy((left_nodes[nid].get("structure_origin"), right_nodes[nid].get("structure_origin")) for nid in sorted(shared)),
        "relation_edge_jaccard": jaccard(_edge_signatures(left), _edge_signatures(right)),
        "node_anchor_jaccard": jaccard(_node_anchor_signatures(left), _node_anchor_signatures(right)),
        "edge_evidence_jaccard": jaccard(_edge_evidence_signatures(left), _edge_evidence_signatures(right)),
    }


def compare_annotations_with_alignment(left: dict, right: dict, alignment: dict) -> dict:
    """Symmetric agreement after an explicit alignment, including split/merge units."""
    left_map, right_map = build_unit_maps(left, right, alignment)
    left_units = collapse_nodes(left, left_map)
    right_units = collapse_nodes(right, right_map)
    shared = set(left_units) & set(right_units)
    non_root = {uid for uid in shared if left_units[uid]["parent_id"] is not None and right_units[uid]["parent_id"] is not None}

    def jaccard(a: set, b: set) -> float:
        union = a | b
        return round(len(a & b) / len(union), 6) if union else 1.0

    left_anchors = {(uid, token) for uid, unit in left_units.items() for token in unit["anchor_tokens"]}
    right_anchors = {(uid, token) for uid, unit in right_units.items() for token in unit["anchor_tokens"]}
    return {
        "shared_units": len(shared),
        "unit_jaccard": jaccard(set(left_units), set(right_units)),
        "hierarchy_parent_agreement": _accuracy((left_units[uid]["parent_id"], right_units[uid]["parent_id"]) for uid in sorted(non_root)),
        "structure_origin_agreement": _accuracy((left_units[uid]["structure_origin"], right_units[uid]["structure_origin"]) for uid in sorted(shared)),
        "relation_edge_jaccard": jaccard(collapsed_edge_signatures(left, left_map), collapsed_edge_signatures(right, right_map)),
        "node_anchor_jaccard": jaccard(left_anchors, right_anchors),
        "edge_evidence_jaccard": jaccard(collapsed_edge_evidence_signatures(left, left_map), collapsed_edge_evidence_signatures(right, right_map)),
        "agreement_mode": "explicit-unit-alignment",
    }
