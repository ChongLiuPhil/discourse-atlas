import test from 'node:test';
import assert from 'node:assert/strict';
import {
  anchorsForSelection,
  paragraphsFromSource,
  projectEdges,
  relatedToAnchor,
  sourceBlocksFromText,
  visibleNodeIds,
} from './model.js';

const document = {
  nodes: [
    { id: 'work', parent_id: null, anchor_ids: [] },
    { id: 'a', parent_id: 'work', anchor_ids: ['p1'] },
    { id: 'b', parent_id: 'work', anchor_ids: ['p2'] },
    { id: 'b1', parent_id: 'b', anchor_ids: ['p3'] },
  ],
  anchors: [{ id: 'p1' }, { id: 'p2' }, { id: 'p3' }],
  edges: [
    { id: 'e1', source: 'a', target: 'b1', evidence_anchor_ids: ['p1', 'p3'] },
  ],
};

test('collapsed descendants are hidden and edges project to the visible parent', () => {
  const visible = visibleNodeIds(document, new Set(['b']));
  assert.equal(visible.has('b1'), false);
  const edges = projectEdges(document, visible);
  assert.equal(edges[0].view_target, 'b');
});

test('anchor relations include both nodes and edges', () => {
  const related = relatedToAnchor(document, 'p3');
  assert.deepEqual([...related.nodeIds], ['b1']);
  assert.deepEqual([...related.edgeIds], ['e1']);
});

test('selection resolves evidence anchors', () => {
  assert.deepEqual(anchorsForSelection(document, { kind: 'edge', id: 'e1' }), ['p1', 'p3']);
});

test('source paragraph numbering ignores markdown headings', () => {
  assert.deepEqual(paragraphsFromSource('# Title\n\nFirst.\n\nSecond.'), ['First.', 'Second.']);
});


test('source blocks retain line ranges for line-based anchors', () => {
  const blocks = sourceBlocksFromText('# Title\n\nFirst line.\ncontinued.\n\nSecond.');
  assert.deepEqual(blocks, [
    { text: 'First line.\ncontinued.', lineStart: 3, lineEnd: 4 },
    { text: 'Second.', lineStart: 6, lineEnd: 6 },
  ]);
});
