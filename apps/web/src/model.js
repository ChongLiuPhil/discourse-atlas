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

function logicalLines(source) {
  const codePoints = Array.from(source);
  const lines = [];
  let start = 0;
  let lineNumber = 1;
  for (let i = 0; i <= codePoints.length; i += 1) {
    const current = codePoints[i];
    if (i !== codePoints.length && current !== '\n' && current !== '\r') continue;
    lines.push({ text: codePoints.slice(start, i).join(''), lineStart: lineNumber, charStart: start, charEnd: i });
    if (current === '\r' && codePoints[i + 1] === '\n') i += 1;
    start = i + 1;
    lineNumber += 1;
  }
  return lines;
}

export function sourceBlocksFromText(source) {
  const lines = logicalLines(source);
  const blocks = [];
  let current = [];
  let page = 1;

  function flush() {
    if (!current.length) return;
    const text = current.map((item) => item.text).join('\n').trim();
    if (text && !/^#{1,6}\s/.test(text)) {
      blocks.push({
        text,
        lineStart: current[0].lineStart,
        lineEnd: current[current.length - 1].lineStart,
        charStart: current[0].charStart,
        charEnd: current[current.length - 1].charEnd,
        pageStart: current[0].page,
        pageEnd: current[current.length - 1].page,
      });
    }
    current = [];
  }

  for (const line of lines) {
    const pageBreaks = (line.text.match(/\f/g) ?? []).length;
    if (pageBreaks) {
      flush();
      page += pageBreaks;
    }
    const text = line.text.replaceAll('\f', '');
    if (!text.trim()) {
      flush();
      continue;
    }
    current.push({ ...line, text, page });
  }
  flush();
  return blocks;
}

export function blockNumbersForAnchor(anchor, blocks) {
  if (!anchor) return [];
  if (Number.isInteger(anchor.paragraph_start)) {
    const end = Number.isInteger(anchor.paragraph_end) ? anchor.paragraph_end : anchor.paragraph_start;
    return blocks.map((_, index) => index + 1).filter((number) => number >= anchor.paragraph_start && number <= end);
  }
  if (Number.isInteger(anchor.line_start)) {
    const end = Number.isInteger(anchor.line_end) ? anchor.line_end : anchor.line_start;
    return blocks.map((block, index) => ({ block, number: index + 1 })).filter(({ block }) => block.lineStart <= end && block.lineEnd >= anchor.line_start).map(({ number }) => number);
  }
  if (Number.isInteger(anchor.char_start) && Number.isInteger(anchor.char_end) && anchor.char_end > anchor.char_start) {
    return blocks.map((block, index) => ({ block, number: index + 1 })).filter(({ block }) => block.charStart < anchor.char_end && block.charEnd > anchor.char_start).map(({ number }) => number);
  }
  if (Number.isInteger(anchor.page_start)) {
    const end = Number.isInteger(anchor.page_end) ? anchor.page_end : anchor.page_start;
    return blocks.map((block, index) => ({ block, number: index + 1 })).filter(({ block }) => block.pageStart <= end && block.pageEnd >= anchor.page_start).map(({ number }) => number);
  }
  return [];
}

export function anchorLocationLabel(anchor) {
  if (!anchor) return '';
  const parts = [];
  if (Number.isInteger(anchor.page_start)) parts.push(`p.${anchor.page_start}${Number.isInteger(anchor.page_end) && anchor.page_end !== anchor.page_start ? `–${anchor.page_end}` : ''}`);
  if (Number.isInteger(anchor.paragraph_start)) parts.push(`¶${anchor.paragraph_start}${Number.isInteger(anchor.paragraph_end) && anchor.paragraph_end !== anchor.paragraph_start ? `–${anchor.paragraph_end}` : ''}`);
  if (Number.isInteger(anchor.line_start)) parts.push(`lines ${anchor.line_start}${Number.isInteger(anchor.line_end) && anchor.line_end !== anchor.line_start ? `–${anchor.line_end}` : ''}`);
  if (Number.isInteger(anchor.char_start) && Number.isInteger(anchor.char_end)) parts.push(`chars ${anchor.char_start}–${anchor.char_end}`);
  return parts.join(' · ');
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
  for (const anchor of document.anchors) {
    for (const [startKey, endKey] of [['paragraph_start', 'paragraph_end'], ['line_start', 'line_end'], ['page_start', 'page_end']]) {
      if (anchor[startKey] != null && anchor[endKey] != null && anchor[startKey] > anchor[endKey]) errors.push(`Anchor ${anchor.id} has invalid ${startKey}/${endKey} range.`);
      if (anchor[startKey] == null && anchor[endKey] != null) errors.push(`Anchor ${anchor.id}: ${endKey} requires ${startKey}.`);
    }
    if (anchor.char_start != null && anchor.char_end != null && anchor.char_start >= anchor.char_end) errors.push(`Anchor ${anchor.id} has invalid char_start/char_end range.`);
    if (anchor.char_start == null && anchor.char_end != null) errors.push(`Anchor ${anchor.id}: char_end requires char_start.`);
  }
  return [...new Set(errors)];
}
