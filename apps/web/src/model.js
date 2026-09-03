export const RELATIONS = [
  'requires',
  'supports',
  'derives',
  'refines',
  'contrasts',
  'objects_to',
  'responds_to',
  'illustrates',
  'sequence',
];

export const DIRECTED_RELATIONS = new Set([
  'requires',
  'supports',
  'derives',
  'refines',
  'objects_to',
  'responds_to',
  'illustrates',
  'sequence',
]);

export function indexDocument(document) {
  const nodeById = new Map(document.nodes.map((node) => [node.id, node]));
  const anchorById = new Map(document.anchors.map((anchor) => [anchor.id, anchor]));
  const children = new Map();
  for (const node of document.nodes) {
    const key = node.parent_id ?? null;
    const items = children.get(key) ?? [];
    items.push(node.id);
    children.set(key, items);
  }
  return { nodeById, anchorById, children };
}

export function descendantsOf(nodeId, children) {
  const result = [];
  const stack = [...(children.get(nodeId) ?? [])];
  while (stack.length) {
    const current = stack.pop();
    result.push(current);
    stack.push(...(children.get(current) ?? []));
  }
  return result;
}

export function visibleNodeIds(document, collapsed) {
  const { nodeById } = indexDocument(document);
  const visible = new Set();
  for (const node of document.nodes) {
    let current = node;
    let hidden = false;
    while (current?.parent_id) {
      if (collapsed.has(current.parent_id)) {
        hidden = true;
        break;
      }
      current = nodeById.get(current.parent_id);
    }
    if (!hidden) visible.add(node.id);
  }
  return visible;
}

export function nearestVisible(nodeId, nodeById, visible) {
  let currentId = nodeId;
  while (currentId && !visible.has(currentId)) {
    currentId = nodeById.get(currentId)?.parent_id ?? null;
  }
  return currentId;
}

export function projectEdges(document, visible) {
  const { nodeById } = indexDocument(document);
  return document.edges
    .map((edge) => {
      const source = nearestVisible(edge.source, nodeById, visible);
      const target = nearestVisible(edge.target, nodeById, visible);
      if (!source || !target || source === target) return null;
      return { ...edge, view_source: source, view_target: target };
    })
    .filter(Boolean);
}

export function relatedToAnchor(document, anchorId) {
  if (!anchorId) return { nodeIds: new Set(), edgeIds: new Set() };
  const nodeIds = new Set(
    document.nodes
      .filter((node) => node.anchor_ids.includes(anchorId))
      .map((node) => node.id),
  );
  const edgeIds = new Set(
    document.edges
      .filter((edge) => edge.evidence_anchor_ids.includes(anchorId))
      .map((edge) => edge.id),
  );
  return { nodeIds, edgeIds };
}

export function anchorsForSelection(document, selection) {
  if (!selection) return [];
  if (selection.kind === 'node') {
    return document.nodes.find((node) => node.id === selection.id)?.anchor_ids ?? [];
  }
  if (selection.kind === 'edge') {
    return document.edges.find((edge) => edge.id === selection.id)?.evidence_anchor_ids ?? [];
  }
  return [];
}

export function sourceBlocksFromText(source) {
  const lines = source.split(/\r?\n/);
  const blocks = [];
  let current = [];
  let startLine = null;

  function flush(endLine) {
    if (!current.length) return;
    const text = current.join('\n').trim();
    if (text && !/^#{1,6}\s/.test(text)) {
      blocks.push({ text, lineStart: startLine, lineEnd: endLine });
    }
    current = [];
    startLine = null;
  }

  lines.forEach((line, index) => {
    const lineNumber = index + 1;
    if (!line.trim()) {
      flush(lineNumber - 1);
      return;
    }
    if (startLine === null) startLine = lineNumber;
    current.push(line);
  });
  flush(lines.length);
  return blocks;
}

export function paragraphsFromSource(source) {
  return sourceBlocksFromText(source).map((block) => block.text);
}

export function validateClientDocument(document) {
  const errors = [];
  if (!document || typeof document !== 'object') return ['Document must be a JSON object.'];
  for (const key of ['schema_version', 'document', 'anchors', 'nodes', 'edges']) {
    if (!(key in document)) errors.push(`Missing top-level field: ${key}`);
  }
  if (!Array.isArray(document.nodes) || document.nodes.length === 0) {
    errors.push('nodes must be a non-empty array.');
    return errors;
  }
  if (!Array.isArray(document.edges) || !Array.isArray(document.anchors)) {
    errors.push('edges and anchors must be arrays.');
    return errors;
  }
  const nodeIds = new Set(document.nodes.map((node) => node.id));
  const anchorIds = new Set(document.anchors.map((anchor) => anchor.id));
  for (const node of document.nodes) {
    if (!node.id || !node.title) errors.push('Every node needs id and title.');
    if (node.parent_id && !nodeIds.has(node.parent_id)) {
      errors.push(`Node ${node.id} references missing parent ${node.parent_id}.`);
    }
    for (const anchorId of node.anchor_ids ?? []) {
      if (!anchorIds.has(anchorId)) errors.push(`Node ${node.id} references missing anchor ${anchorId}.`);
    }
  }
  for (const edge of document.edges) {
    if (!nodeIds.has(edge.source) || !nodeIds.has(edge.target)) {
      errors.push(`Edge ${edge.id} references a missing endpoint.`);
    }
    if (!RELATIONS.includes(edge.relation)) errors.push(`Edge ${edge.id} uses unknown relation ${edge.relation}.`);
  }
  return [...new Set(errors)];
}
