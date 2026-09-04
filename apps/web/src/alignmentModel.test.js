import test from 'node:test';
import assert from 'node:assert/strict';
import { addReviewedUnit, alignmentCoverage, proposeAlignment, refreshUnmatched, updateUnit, validateWorkbenchAlignment } from './alignmentModel.js';

function doc(ids = ['work', 'a', 'b']) {
  const [work, a, b] = ids;
  return {
    anchors: [
      { id: 'p1', paragraph_start: 1, paragraph_end: 1 },
      { id: 'p2', paragraph_start: 2, paragraph_end: 2 },
      { id: 'p3', paragraph_start: 3, paragraph_end: 3 },
    ],
    nodes: [
      { id: work, parent_id: null, kind: 'work', anchor_ids: ['p1', 'p2', 'p3'] },
      { id: a, parent_id: work, kind: 'section', anchor_ids: ['p1'] },
      { id: b, parent_id: work, kind: 'section', anchor_ids: ['p2', 'p3'] },
    ],
  };
}

test('anchor proposal aligns renamed units deterministically', () => {
  const alignment = proposeAlignment(doc(), doc(['root', 'alpha', 'beta']));
  assert.equal(alignment.units.length, 3);
  assert.deepEqual(alignment.unmatched_reference_node_ids, []);
  assert.deepEqual(alignment.unmatched_candidate_node_ids, []);
});

test('reviewer can create explicit split-merge unit', () => {
  let alignment = { alignment_version: '0.1.0', units: [] };
  alignment = addReviewedUnit(alignment, ['a', 'b'], ['alpha'], 'same source span');
  assert.equal(alignment.units[0].method, 'manual-split-merge');
  assert.equal(alignment.units[0].status, 'accepted');
});

test('rejected proposals stop counting as mapped and refresh unmatched', () => {
  const reference = doc();
  const candidate = doc(['root', 'alpha', 'beta']);
  let alignment = proposeAlignment(reference, candidate);
  alignment = updateUnit(alignment, alignment.units[0].unit_id, { status: 'rejected' });
  alignment = refreshUnmatched(reference, candidate, alignment);
  const coverage = alignmentCoverage(reference, candidate, alignment);
  assert.equal(coverage.referenceMapped, 2);
  assert.equal(alignment.unmatched_reference_node_ids.length, 1);
});

test('workbench validation detects duplicate membership', () => {
  const reference = doc();
  const candidate = doc(['root', 'alpha', 'beta']);
  const alignment = { alignment_version: '0.1.0', units: [
    { unit_id: 'u1', reference_node_ids: ['a'], candidate_node_ids: ['alpha'], status: 'accepted' },
    { unit_id: 'u2', reference_node_ids: ['a'], candidate_node_ids: ['beta'], status: 'accepted' },
  ] };
  assert.ok(validateWorkbenchAlignment(reference, candidate, alignment).some((error) => error.includes('mapped more than once')));
});
