from __future__ import annotations

from collections import defaultdict


CHAR_CELL_SIZE = 32


def _inclusive_tokens(prefix: str, start: object, end: object) -> set[tuple[str, object]]:
    if not isinstance(start, int):
        return set()
    finish = end if isinstance(end, int) else start
    return {(prefix, value) for value in range(start, finish + 1)}


def _character_tokens(start: object, end: object) -> set[tuple[str, object]]:
    """Return scalable overlap cells for 0-based, end-exclusive Unicode code-point spans."""
    if not isinstance(start, int) or not isinstance(end, int) or end <= start:
        return set()
    first = start // CHAR_CELL_SIZE
    last = (end - 1) // CHAR_CELL_SIZE
    return {("c32", value) for value in range(first, last + 1)}


def _anchor_tokens(anchor: dict) -> set[tuple[str, object]]:
    # Preserve v0.5 behavior when paragraph/line coordinates are available.
    tokens = _inclusive_tokens("p", anchor.get("paragraph_start"), anchor.get("paragraph_end"))
    tokens.update(_inclusive_tokens("l", anchor.get("line_start"), anchor.get("line_end")))
    if tokens:
        return tokens

    # Character offsets are more precise than page numbers and remain edition-specific.
    tokens = _character_tokens(anchor.get("char_start"), anchor.get("char_end"))
    if tokens:
        return tokens

    tokens = _inclusive_tokens("pg", anchor.get("page_start"), anchor.get("page_end"))
    if tokens:
        return tokens

    if anchor.get("section_label"):
        return {("s", str(anchor["section_label"]))}
    return set()


def anchor_map(document: dict) -> dict[str, dict]:
    return {anchor["id"]: anchor for anchor in document.get("anchors", [])}


def node_footprint(document: dict, node: dict) -> set[tuple[str, object]]:
    anchors = anchor_map(document)
    tokens: set[tuple[str, object]] = set()
    for anchor_id in node.get("anchor_ids", []):
        anchor = anchors.get(anchor_id)
        if anchor:
            tokens.update(_anchor_tokens(anchor))
    return tokens


def edge_evidence_footprint(document: dict, edge: dict) -> set[tuple[str, object]]:
    anchors = anchor_map(document)
    tokens: set[tuple[str, object]] = set()
    for anchor_id in edge.get("evidence_anchor_ids", []):
        anchor = anchors.get(anchor_id)
        if anchor:
            tokens.update(_anchor_tokens(anchor))
    return tokens


def _jaccard(left: set, right: set) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def propose_alignment(reference: dict, candidate: dict, threshold: float = 0.5) -> dict:
    """Propose an inspectable one-to-one unit alignment using stable IDs and source anchors.

    No embeddings or model calls are used. Split/merge alignments remain explicit manual edits:
    a user may put multiple IDs from either side into one alignment unit.
    """
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")

    ref_nodes = {node["id"]: node for node in reference.get("nodes", [])}
    cand_nodes = {node["id"]: node for node in candidate.get("nodes", [])}
    matched_ref: set[str] = set()
    matched_cand: set[str] = set()
    units: list[dict] = []

    def add_unit(ref_id: str, cand_id: str, method: str, score: float) -> None:
        units.append({
            "unit_id": f"u-{len(units)+1:03d}",
            "reference_node_ids": [ref_id],
            "candidate_node_ids": [cand_id],
            "method": method,
            "confidence": round(score, 6),
            "status": "proposed",
        })
        matched_ref.add(ref_id)
        matched_cand.add(cand_id)

    ref_roots = [n for n in ref_nodes.values() if n.get("parent_id") is None and n.get("kind") == "work"]
    cand_roots = [n for n in cand_nodes.values() if n.get("parent_id") is None and n.get("kind") == "work"]
    if len(ref_roots) == 1 and len(cand_roots) == 1:
        add_unit(ref_roots[0]["id"], cand_roots[0]["id"], "root-kind", 1.0)

    for node_id in sorted(set(ref_nodes) & set(cand_nodes)):
        if node_id not in matched_ref and node_id not in matched_cand:
            add_unit(node_id, node_id, "stable-id", 1.0)

    candidates: list[tuple[float, str, str]] = []
    for ref_id, ref_node in ref_nodes.items():
        if ref_id in matched_ref:
            continue
        ref_fp = node_footprint(reference, ref_node)
        if not ref_fp:
            continue
        for cand_id, cand_node in cand_nodes.items():
            if cand_id in matched_cand:
                continue
            cand_fp = node_footprint(candidate, cand_node)
            if not cand_fp:
                continue
            score = _jaccard(ref_fp, cand_fp)
            if score >= threshold:
                candidates.append((score, ref_id, cand_id))

    for score, ref_id, cand_id in sorted(candidates, key=lambda item: (-item[0], item[1], item[2])):
        if ref_id in matched_ref or cand_id in matched_cand:
            continue
        add_unit(ref_id, cand_id, "anchor-overlap", score)

    return {
        "alignment_version": "0.1.0",
        "method": "deterministic-anchor-overlap",
        "threshold": threshold,
        "units": units,
        "unmatched_reference_node_ids": sorted(set(ref_nodes) - matched_ref),
        "unmatched_candidate_node_ids": sorted(set(cand_nodes) - matched_cand),
    }


def validate_alignment(alignment: dict, reference: dict, candidate: dict) -> list[str]:
    errors: list[str] = []
    ref_ids = {node["id"] for node in reference.get("nodes", [])}
    cand_ids = {node["id"] for node in candidate.get("nodes", [])}
    seen_units: set[str] = set()
    seen_ref: set[str] = set()
    seen_cand: set[str] = set()

    for unit in alignment.get("units", []):
        unit_id = unit.get("unit_id")
        if not isinstance(unit_id, str) or not unit_id:
            errors.append("alignment unit missing non-empty unit_id")
            continue
        if unit_id in seen_units:
            errors.append(f"duplicate alignment unit_id: {unit_id}")
        seen_units.add(unit_id)
        if unit.get("status") == "rejected":
            continue
        ref_members = unit.get("reference_node_ids", [])
        cand_members = unit.get("candidate_node_ids", [])
        if not ref_members or not cand_members:
            errors.append(f"unit {unit_id}: accepted/proposed unit must contain nodes on both sides")
        for node_id in ref_members:
            if node_id not in ref_ids:
                errors.append(f"unit {unit_id}: unknown reference node {node_id}")
            if node_id in seen_ref:
                errors.append(f"reference node appears in multiple units: {node_id}")
            seen_ref.add(node_id)
        for node_id in cand_members:
            if node_id not in cand_ids:
                errors.append(f"unit {unit_id}: unknown candidate node {node_id}")
            if node_id in seen_cand:
                errors.append(f"candidate node appears in multiple units: {node_id}")
            seen_cand.add(node_id)
    return sorted(set(errors))


def build_unit_maps(reference: dict, candidate: dict, alignment: dict) -> tuple[dict[str, str], dict[str, str]]:
    errors = validate_alignment(alignment, reference, candidate)
    if errors:
        raise ValueError("; ".join(errors))
    ref_map: dict[str, str] = {}
    cand_map: dict[str, str] = {}
    for unit in alignment.get("units", []):
        if unit.get("status") == "rejected":
            continue
        unit_id = unit["unit_id"]
        for node_id in unit.get("reference_node_ids", []):
            ref_map[node_id] = unit_id
        for node_id in unit.get("candidate_node_ids", []):
            cand_map[node_id] = unit_id
    for node in reference.get("nodes", []):
        ref_map.setdefault(node["id"], f"__reference__:{node['id']}")
    for node in candidate.get("nodes", []):
        cand_map.setdefault(node["id"], f"__candidate__:{node['id']}")
    return ref_map, cand_map


def collapse_nodes(document: dict, node_to_unit: dict[str, str]) -> dict[str, dict]:
    nodes = {node["id"]: node for node in document.get("nodes", [])}
    members: dict[str, list[str]] = defaultdict(list)
    for node_id, unit_id in node_to_unit.items():
        if node_id in nodes:
            members[unit_id].append(node_id)

    collapsed: dict[str, dict] = {}
    for unit_id, member_ids in members.items():
        member_set = set(member_ids)
        parent_units: set[str] = set()
        origins: set[str] = set()
        footprint: set[tuple[str, object]] = set()
        for node_id in member_ids:
            node = nodes[node_id]
            if node.get("structure_origin") is not None:
                origins.add(node.get("structure_origin"))
            footprint.update(node_footprint(document, node))
            parent_id = node.get("parent_id")
            visited: set[str] = set()
            while parent_id is not None and parent_id in member_set and parent_id not in visited:
                visited.add(parent_id)
                parent_id = nodes.get(parent_id, {}).get("parent_id")
            if parent_id is not None:
                parent_units.add(node_to_unit.get(parent_id, f"__missing__:{parent_id}"))
        if len(parent_units) == 0:
            parent_value: object = None
        elif len(parent_units) == 1:
            parent_value = next(iter(parent_units))
        else:
            parent_value = tuple(sorted(parent_units))
        collapsed[unit_id] = {
            "id": unit_id,
            "member_ids": tuple(sorted(member_ids)),
            "parent_id": parent_value,
            "structure_origin": next(iter(origins)) if len(origins) == 1 else ("mixed" if origins else None),
            "anchor_tokens": footprint,
        }
    return collapsed


def collapsed_edge_signatures(document: dict, node_to_unit: dict[str, str]) -> set[tuple[str, str, str]]:
    result: set[tuple[str, str, str]] = set()
    for edge in document.get("edges", []):
        source = node_to_unit.get(edge["source"])
        target = node_to_unit.get(edge["target"])
        if source is None or target is None or source == target:
            continue
        relation = edge["relation"]
        if relation == "contrasts":
            source, target = sorted((source, target))
        result.add((source, target, relation))
    return result


def collapsed_edge_evidence_signatures(document: dict, node_to_unit: dict[str, str]) -> set[tuple[str, str, str, tuple[str, object]]]:
    result: set[tuple[str, str, str, tuple[str, object]]] = set()
    for edge in document.get("edges", []):
        source = node_to_unit.get(edge["source"])
        target = node_to_unit.get(edge["target"])
        if source is None or target is None or source == target:
            continue
        relation = edge["relation"]
        if relation == "contrasts":
            source, target = sorted((source, target))
        for token in edge_evidence_footprint(document, edge):
            result.add((source, target, relation, token))
    return result
