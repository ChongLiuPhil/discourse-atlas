export function indexNodes(document) {
  return new Map((document?.nodes ?? []).map((node) => [node.id, node]));
}

export function anchorTokens(anchor) {
  const tokens = new Set();
  const addRange = (prefix, start, end) => {
    if (!Number.isInteger(start)) return;
    const finish = Number.isInteger(end) ? end : start;
    for (let value = start; value <= finish; value += 1) tokens.add(`${prefix}:${value}`);
  };
  addRange('p', anchor?.paragraph_start, anchor?.paragraph_end);
  addRange('l', anchor?.line_start, anchor?.line_end);
  if (!tokens.size && anchor?.section_label) tokens.add(`s:${anchor.section_label}`);
  return tokens;
}

function anchorIndex(document) {
  return new Map((document?.anchors ?? []).map((anchor) => [anchor.id, anchor]));
}

export function nodeFootprint(document, node) {
  const anchors = anchorIndex(document);
  const tokens = new Set();
  for (const anchorId of node?.anchor_ids ?? []) {
    const anchor = anchors.get(anchorId);
    if (!anchor) continue;
    for (const token of anchorTokens(anchor)) tokens.add(token);
  }
  return tokens;
}

export function jaccard(left, right) {
  const union = new Set([...left, ...right]);
  if (!union.size) return 0;
  let overlap = 0;
  for (const item of left) if (right.has(item)) overlap += 1;
  return overlap / union.size;
}

export function proposeAlignment(reference, candidate, threshold = 0.5) {
  if (threshold < 0 || threshold > 1) throw new Error('threshold must be between 0 and 1');
  const refNodes = indexNodes(reference);
  const candNodes = indexNodes(candidate);
  const matchedRef = new Set();
  const matchedCand = new Set();
  const units = [];
  const add = (refId, candId, method, confidence) => {
    units.push({ unit_id: `u-${String(units.length + 1).padStart(3, '0')}`, reference_node_ids: [refId], candidate_node_ids: [candId], method, confidence: Number(confidence.toFixed(6)), status: 'proposed' });
    matchedRef.add(refId);
    matchedCand.add(candId);
  };
  const refRoots = [...refNodes.values()].filter((node) => node.parent_id == null && node.kind === 'work');
  const candRoots = [...candNodes.values()].filter((node) => node.parent_id == null && node.kind === 'work');
  if (refRoots.length === 1 && candRoots.length === 1) add(refRoots[0].id, candRoots[0].id, 'root-kind', 1);
  for (const id of [...refNodes.keys()].filter((id) => candNodes.has(id)).sort()) {
    if (!matchedRef.has(id) && !matchedCand.has(id)) add(id, id, 'stable-id', 1);
  }
  const candidates = [];
  for (const [refId, refNode] of refNodes) {
    if (matchedRef.has(refId)) continue;
    const refFootprint = nodeFootprint(reference, refNode);
    if (!refFootprint.size) continue;
    for (const [candId, candNode] of candNodes) {
      if (matchedCand.has(candId)) continue;
      const candFootprint = nodeFootprint(candidate, candNode);
      if (!candFootprint.size) continue;
      const score = jaccard(refFootprint, candFootprint);
      if (score >= threshold) candidates.push({ score, refId, candId });
    }
  }
  candidates.sort((a, b) => b.score - a.score || a.refId.localeCompare(b.refId) || a.candId.localeCompare(b.candId));
  for (const { score, refId, candId } of candidates) {
    if (!matchedRef.has(refId) && !matchedCand.has(candId)) add(refId, candId, 'anchor-overlap', score);
  }
  return { alignment_version: '0.1.0', method: 'deterministic-anchor-overlap', threshold, units, unmatched_reference_node_ids: [...refNodes.keys()].filter((id) => !matchedRef.has(id)).sort(), unmatched_candidate_node_ids: [...candNodes.keys()].filter((id) => !matchedCand.has(id)).sort() };
}

export function mappedNodeIds(alignment, side) {
  const key = side === 'reference' ? 'reference_node_ids' : 'candidate_node_ids';
  const result = new Set();
  for (const unit of alignment?.units ?? []) {
    if (unit.status === 'rejected') continue;
    for (const id of unit[key] ?? []) result.add(id);
  }
  return result;
}

export function alignmentCoverage(reference, candidate, alignment) {
  const refMapped = mappedNodeIds(alignment, 'reference');
  const candMapped = mappedNodeIds(alignment, 'candidate');
  const refTotal = reference?.nodes?.length ?? 0;
  const candTotal = candidate?.nodes?.length ?? 0;
  return { referenceMapped: refMapped.size, referenceTotal: refTotal, candidateMapped: candMapped.size, candidateTotal: candTotal, referenceRatio: refTotal ? refMapped.size / refTotal : 1, candidateRatio: candTotal ? candMapped.size / candTotal : 1 };
}

export function addReviewedUnit(alignment, referenceNodeIds, candidateNodeIds, rationale = '') {
  if (!referenceNodeIds.length || !candidateNodeIds.length) throw new Error('Select at least one node on each side');
  const usedReference = mappedNodeIds(alignment, 'reference');
  const usedCandidate = mappedNodeIds(alignment, 'candidate');
  const duplicateReference = referenceNodeIds.find((id) => usedReference.has(id));
  const duplicateCandidate = candidateNodeIds.find((id) => usedCandidate.has(id));
  if (duplicateReference) throw new Error(`Reference node already mapped: ${duplicateReference}`);
  if (duplicateCandidate) throw new Error(`Candidate node already mapped: ${duplicateCandidate}`);
  const existing = new Set((alignment?.units ?? []).map((unit) => unit.unit_id));
  let index = (alignment?.units?.length ?? 0) + 1;
  let unitId = `u-review-${String(index).padStart(3, '0')}`;
  while (existing.has(unitId)) { index += 1; unitId = `u-review-${String(index).padStart(3, '0')}`; }
  return { ...alignment, units: [...(alignment?.units ?? []), { unit_id: unitId, reference_node_ids: [...referenceNodeIds], candidate_node_ids: [...candidateNodeIds], method: referenceNodeIds.length === 1 && candidateNodeIds.length === 1 ? 'manual' : 'manual-split-merge', confidence: 1, status: 'accepted', ...(rationale ? { rationale } : {}) }] };
}

export function updateUnit(alignment, unitId, patch) {
  return { ...alignment, units: (alignment?.units ?? []).map((unit) => unit.unit_id === unitId ? { ...unit, ...patch } : unit) };
}

export function removeUnit(alignment, unitId) {
  return { ...alignment, units: (alignment?.units ?? []).filter((unit) => unit.unit_id !== unitId) };
}

export function refreshUnmatched(reference, candidate, alignment) {
  const refMapped = mappedNodeIds(alignment, 'reference');
  const candMapped = mappedNodeIds(alignment, 'candidate');
  return { ...alignment, unmatched_reference_node_ids: (reference?.nodes ?? []).map((node) => node.id).filter((id) => !refMapped.has(id)).sort(), unmatched_candidate_node_ids: (candidate?.nodes ?? []).map((node) => node.id).filter((id) => !candMapped.has(id)).sort() };
}

export function validateWorkbenchAlignment(reference, candidate, alignment) {
  const errors = [];
  const refIds = new Set((reference?.nodes ?? []).map((node) => node.id));
  const candIds = new Set((candidate?.nodes ?? []).map((node) => node.id));
  const seenUnits = new Set();
  const seenRef = new Set();
  const seenCand = new Set();
  for (const unit of alignment?.units ?? []) {
    if (!unit.unit_id) errors.push('Alignment unit missing unit_id');
    if (seenUnits.has(unit.unit_id)) errors.push(`Duplicate unit ID: ${unit.unit_id}`);
    seenUnits.add(unit.unit_id);
    if (unit.status === 'rejected') continue;
    if (!(unit.reference_node_ids ?? []).length || !(unit.candidate_node_ids ?? []).length) errors.push(`${unit.unit_id}: both sides are required`);
    for (const id of unit.reference_node_ids ?? []) { if (!refIds.has(id)) errors.push(`${unit.unit_id}: unknown reference node ${id}`); if (seenRef.has(id)) errors.push(`Reference node mapped more than once: ${id}`); seenRef.add(id); }
    for (const id of unit.candidate_node_ids ?? []) { if (!candIds.has(id)) errors.push(`${unit.unit_id}: unknown candidate node ${id}`); if (seenCand.has(id)) errors.push(`Candidate node mapped more than once: ${id}`); seenCand.add(id); }
  }
  return [...new Set(errors)].sort();
}
