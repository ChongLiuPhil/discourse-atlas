import ELK from 'elkjs/lib/elk.bundled.js';
import { indexDocument } from './model.js';

const elk = new ELK();
const LEAF_WIDTH = 310;
const LEAF_HEIGHT = 150;
const COLLAPSED_WIDTH = 330;
const COLLAPSED_HEIGHT = 160;

function elkNode(node, children, visible, collapsed) {
  const childIds = (children.get(node.id) ?? []).filter((id) => visible.has(id));
  const hasVisibleChildren = childIds.length > 0 && !collapsed.has(node.id);
  const result = {
    id: node.id,
    layoutOptions: hasVisibleChildren
      ? {
          'elk.padding': '[top=72,left=28,bottom=28,right=28]',
          'elk.spacing.nodeNode': '48',
        }
      : undefined,
  };
  if (hasVisibleChildren) {
    result.children = childIds.map((id) => elkNode(children.nodeById.get(id), children, visible, collapsed));
  } else {
    result.width = collapsed.has(node.id) ? COLLAPSED_WIDTH : LEAF_WIDTH;
    result.height = collapsed.has(node.id) ? COLLAPSED_HEIGHT : LEAF_HEIGHT;
  }
  return result;
}

function flattenLayout(node, parentId = null, result = []) {
  if (node.id !== '__root__') {
    result.push({
      id: node.id,
      parentId,
      x: node.x ?? 0,
      y: node.y ?? 0,
      width: node.width ?? LEAF_WIDTH,
      height: node.height ?? LEAF_HEIGHT,
      hasChildren: Boolean(node.children?.length),
    });
  }
  for (const child of node.children ?? []) {
    flattenLayout(child, node.id === '__root__' ? null : node.id, result);
  }
  return result;
}

export async function layoutDocument(document, visible, collapsed, projectedEdges) {
  const index = indexDocument(document);
  const roots = (index.children.get(null) ?? []).filter((id) => visible.has(id));
  const helper = index.children;
  helper.nodeById = index.nodeById;
  const graph = {
    id: '__root__',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': 'DOWN',
      'elk.hierarchyHandling': 'INCLUDE_CHILDREN',
      'elk.edgeRouting': 'ORTHOGONAL',
      'elk.spacing.nodeNode': '70',
      'elk.layered.spacing.nodeNodeBetweenLayers': '100',
      'elk.layered.crossingMinimization.greedySwitch.type': 'TWO_SIDED',
      'elk.padding': '[top=36,left=36,bottom=36,right=36]',
    },
    children: roots.map((id) => elkNode(index.nodeById.get(id), helper, visible, collapsed)),
    edges: projectedEdges.map((edge) => ({
      id: `elk-${edge.id}`,
      sources: [edge.view_source],
      targets: [edge.view_target],
    })),
  };
  const laidOut = await elk.layout(graph);
  return flattenLayout(laidOut);
}
