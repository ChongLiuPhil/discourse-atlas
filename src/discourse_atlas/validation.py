from __future__ import annotations

from collections import Counter


def _duplicates(values: list[str]) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def _check_range(item: dict, start_key: str, end_key: str, label: str) -> list[str]:
    start = item.get(start_key)
    end = item.get(end_key)
    if start is not None and end is not None and start > end:
        return [f"{label}: {start_key} must be <= {end_key}"]
    return []


def validate_references(document: dict) -> list[str]:
    """Validate graph invariants that JSON Schema cannot express cleanly."""
    errors: list[str] = []

    anchors = document.get("anchors", [])
    nodes = document.get("nodes", [])
    edges = document.get("edges", [])

    anchor_ids = [item.get("id") for item in anchors if isinstance(item.get("id"), str)]
    node_ids = [item.get("id") for item in nodes if isinstance(item.get("id"), str)]
    edge_ids = [item.get("id") for item in edges if isinstance(item.get("id"), str)]

    for label, values in (("anchor", anchor_ids), ("node", node_ids), ("edge", edge_ids)):
        for duplicate in _duplicates(values):
            errors.append(f"duplicate {label} id: {duplicate}")

    anchor_set = set(anchor_ids)
    node_set = set(node_ids)

    roots = [node for node in nodes if node.get("parent_id") is None]
    work_roots = [node for node in roots if node.get("kind") == "work"]
    if len(roots) != 1 or len(work_roots) != 1:
        errors.append("containment hierarchy must have exactly one root node of kind 'work'")

    parents: dict[str, str | None] = {}
    for node in nodes:
        node_id = node.get("id")
        if not isinstance(node_id, str):
            continue
        parent_id = node.get("parent_id")
        parents[node_id] = parent_id if isinstance(parent_id, str) else None

        if parent_id == node_id:
            errors.append(f"node {node_id}: parent_id cannot reference itself")
        elif parent_id is not None and parent_id not in node_set:
            errors.append(f"node {node_id}: unknown parent_id {parent_id}")

        for anchor_id in node.get("anchor_ids", []):
            if anchor_id not in anchor_set:
                errors.append(f"node {node_id}: unknown anchor_id {anchor_id}")

    # Parent links must form an acyclic hierarchy.
    for node_id in node_ids:
        seen: set[str] = set()
        current: str | None = node_id
        while current is not None and current in parents:
            if current in seen:
                errors.append(f"containment cycle detected involving node {current}")
                break
            seen.add(current)
            current = parents[current]

    for edge in edges:
        edge_id = edge.get("id", "<unknown>")
        source = edge.get("source")
        target = edge.get("target")
        if source not in node_set:
            errors.append(f"edge {edge_id}: unknown source node {source}")
        if target not in node_set:
            errors.append(f"edge {edge_id}: unknown target node {target}")
        if source == target:
            errors.append(f"edge {edge_id}: self-relations are not allowed")
        for anchor_id in edge.get("evidence_anchor_ids", []):
            if anchor_id not in anchor_set:
                errors.append(f"edge {edge_id}: unknown evidence anchor {anchor_id}")

    for anchor in anchors:
        anchor_id = anchor.get("id", "<unknown>")
        errors.extend(_check_range(anchor, "paragraph_start", "paragraph_end", f"anchor {anchor_id}"))
        errors.extend(_check_range(anchor, "line_start", "line_end", f"anchor {anchor_id}"))

    return sorted(set(errors))
