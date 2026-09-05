import test from 'node:test';
import assert from 'node:assert/strict';
import {
  anchorsForSelection,
  blockNumbersForAnchor,
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

test('source blocks retain line, code-point character, and page ranges', () => {
  const blocks = sourceBlocksFromText('# Title\n\nFirst line.\ncontinued.\n\nSecond.');
  assert.deepEqual(blocks, [
    { text: 'First line.\ncontinued.', lineStart: 3, lineEnd: 4, charStart: 9, charEnd: 31, pageStart: 1, pageEnd: 1 },
    { text: 'Second.', lineStart: 6, lineEnd: 6, charStart: 33, charEnd: 40, pageStart: 1, pageEnd: 1 },
  ]);
});

test('character coordinates count Unicode code points rather than UTF-16 units', () => {
  const [block] = sourceBlocksFromText('A🙂中B');
  assert.equal(block.charStart, 0);
  assert.equal(block.charEnd, 4);
  assert.deepEqual(blockNumbersForAnchor({ char_start: 1, char_end: 3 }, [block]), [1]);
});

test('form-feed boundaries make page-only anchors traceable', () => {
  const blocks = sourceBlocksFromText('First.\n\f\nSecond.');
  assert.equal(blocks[0].pageStart, 1);
  assert.equal(blocks[1].pageStart, 2);
  assert.deepEqual(blockNumbersForAnchor({ page_start: 2, page_end: 2 }, blocks), [2]);
});

test('paragraph and line anchors retain navigation priority over character coordinates', () => {
  const blocks = sourceBlocksFromText('First.\n\nSecond.');
  assert.deepEqual(blockNumbersForAnchor({ paragraph_start: 2, char_start: 0, char_end: 3 }, blocks), [2]);
});
