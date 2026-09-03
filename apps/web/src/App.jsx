import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Background,
  Controls,
  MarkerType,
  MiniMap,
  ReactFlow,
  ReactFlowProvider,
  useReactFlow,
} from '@xyflow/react';
import { ContainerNode, DiscourseNode } from './components/DiscourseNode.jsx';
import SourcePanel from './components/SourcePanel.jsx';
import Inspector from './components/Inspector.jsx';
import { layoutDocument } from './layout.js';
import {
  DIRECTED_RELATIONS,
  anchorsForSelection,
  descendantsOf,
  indexDocument,
  projectEdges,
  relatedToAnchor,
  validateClientDocument,
  visibleNodeIds,
} from './model.js';

const nodeTypes = { discourse: DiscourseNode, container: ContainerNode };

function AppInner() {
  const [document, setDocument] = useState(null);
  const [source, setSource] = useState('');
  const [collapsed, setCollapsed] = useState(new Set());
  const [selection, setSelection] = useState(null);
  const [focusAnchorId, setFocusAnchorId] = useState(null);
  const [layoutNodes, setLayoutNodes] = useState([]);
  const [status, setStatus] = useState('Loading example…');
  const [loadErrors, setLoadErrors] = useState([]);
  const reactFlow = useReactFlow();
  const layoutGeneration = useRef(0);

  const index = useMemo(() => document ? indexDocument(document) : null, [document]);
  const activeAnchorIds = useMemo(() => new Set([
    ...anchorsForSelection(document ?? { nodes: [], edges: [] }, selection),
    ...(focusAnchorId ? [focusAnchorId] : []),
  ]), [document, selection, focusAnchorId]);
  const anchorRelated = useMemo(() => document ? relatedToAnchor(document, focusAnchorId) : { nodeIds: new Set(), edgeIds: new Set() }, [document, focusAnchorId]);

  const visible = useMemo(() => document ? visibleNodeIds(document, collapsed) : new Set(), [document, collapsed]);
  const projectedEdges = useMemo(() => document ? projectEdges(document, visible) : [], [document, visible]);

  const toggleCollapse = useCallback((id) => {
    setCollapsed((current) => {
      const next = new Set(current);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }, []);

  const runLayout = useCallback(async () => {
    if (!document || !index) return;
    const generation = ++layoutGeneration.current;
    setStatus('Laying out graph…');
    try {
      const result = await layoutDocument(document, visible, collapsed, projectedEdges);
      if (generation !== layoutGeneration.current) return;
      setLayoutNodes(result);
      setStatus(`${document.nodes.length} nodes · ${document.edges.length} relations`);
      requestAnimationFrame(() => reactFlow.fitView({ padding: 0.12, duration: 350 }));
    } catch (error) {
      console.error(error);
      setStatus('Layout failed');
      setLoadErrors([String(error)]);
    }
  }, [document, index, visible, collapsed, projectedEdges, reactFlow]);

  useEffect(() => { runLayout(); }, [runLayout]);

  const flowNodes = useMemo(() => {
    if (!document || !index) return [];
    return layoutNodes.map((layout) => {
      const node = index.nodeById.get(layout.id);
      const childIds = index.children.get(node.id) ?? [];
      const hiddenCount = descendantsOf(node.id, index.children).length;
      const hasVisibleChildren = layout.hasChildren && !collapsed.has(node.id);
      const highlighted = focusAnchorId ? anchorRelated.nodeIds.has(node.id) : false;
      const dimmed = focusAnchorId ? !highlighted : false;
      return {
        id: node.id,
        type: hasVisibleChildren ? 'container' : 'discourse',
        parentId: layout.parentId ?? undefined,
        extent: layout.parentId ? 'parent' : undefined,
        position: { x: layout.x, y: layout.y },
        style: { width: layout.width, height: layout.height },
        data: {
          ...node,
          id: node.id,
          collapsible: childIds.length > 0,
          collapsed: collapsed.has(node.id),
          hiddenCount,
          highlighted,
          dimmed,
          onToggleCollapse: toggleCollapse,
        },
      };
    });
  }, [document, index, layoutNodes, collapsed, focusAnchorId, anchorRelated, toggleCollapse]);

  const flowEdges = useMemo(() => projectedEdges.map((edge) => {
    const selected = selection?.kind === 'edge' && selection.id === edge.id;
    const highlighted = focusAnchorId ? anchorRelated.edgeIds.has(edge.id) : false;
    const dimmed = focusAnchorId ? !highlighted : false;
    const directed = DIRECTED_RELATIONS.has(edge.relation);
    return {
      id: `view-${edge.id}`,
      source: edge.view_source,
      target: edge.view_target,
      type: 'smoothstep',
      label: edge.relation.replaceAll('_', ' '),
      animated: selected,
      markerEnd: directed ? { type: MarkerType.ArrowClosed } : undefined,
      style: {
        strokeWidth: selected || highlighted ? 3 : 1.8,
        opacity: dimmed ? 0.18 : 0.9,
        strokeDasharray: edge.relation === 'sequence' ? '7 6' : undefined,
      },
      labelStyle: { fontSize: 12, fontWeight: 650 },
      data: { edgeId: edge.id },
    };
  }), [projectedEdges, selection, focusAnchorId, anchorRelated]);

  async function loadExample() {
    try {
      const [analysisResponse, sourceResponse] = await Promise.all([
        fetch('./example-analysis.json'),
        fetch('./example-source.md'),
      ]);
      const nextDocument = await analysisResponse.json();
      const nextSource = await sourceResponse.text();
      loadDocument(nextDocument, nextSource);
    } catch (error) {
      setLoadErrors([`Could not load bundled example: ${error}`]);
    }
  }

  useEffect(() => { loadExample(); }, []);

  function loadDocument(nextDocument, nextSource = source) {
    const errors = validateClientDocument(nextDocument);
    setLoadErrors(errors);
    if (errors.length) return;
    setDocument(nextDocument);
    setSource(nextSource ?? '');
    setCollapsed(new Set());
    setSelection(null);
    setFocusAnchorId(null);
  }

  async function handleAnalysisUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const parsed = JSON.parse(await file.text());
      loadDocument(parsed);
    } catch (error) {
      setLoadErrors([`Invalid JSON: ${error}`]);
    } finally {
      event.target.value = '';
    }
  }

  async function handleSourceUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setSource(await file.text());
    event.target.value = '';
  }

  function downloadDocument() {
    if (!document) return;
    const blob = new Blob([`${JSON.stringify(document, null, 2)}\n`], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = Object.assign(window.document.createElement('a'), { href: url, download: 'analysis.corrected.json' });
    link.click();
    URL.revokeObjectURL(url);
  }

  if (!document) {
    return <main className="loading-screen"><h1>Discourse Atlas</h1><p>{status}</p>{loadErrors.map((error) => <p className="error" key={error}>{error}</p>)}</main>;
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">DA</div>
          <div><strong>Discourse Atlas</strong><span>{document.document.title}</span></div>
        </div>
        <div className="toolbar">
          <span className="status">{status}</span>
          <label className="file-button">Open analysis<input type="file" accept="application/json,.json" onChange={handleAnalysisUpload} /></label>
          <label className="file-button">Open source<input type="file" accept="text/plain,text/markdown,.md,.txt" onChange={handleSourceUpload} /></label>
          <button onClick={downloadDocument}>Export corrections</button>
          <button onClick={runLayout}>Relayout</button>
        </div>
      </header>

      {loadErrors.length ? <div className="error-banner">{loadErrors.join(' ')}</div> : null}

      <main className="workspace">
        <section className="panel source-panel">
          <div className="panel-heading"><div><span className="eyebrow">Source</span><h1>Close reading</h1></div><button onClick={() => setFocusAnchorId(null)}>Clear focus</button></div>
          <SourcePanel
            source={source}
            anchors={document.anchors}
            activeAnchorIds={activeAnchorIds}
            focusAnchorId={focusAnchorId}
            onAnchorFocus={setFocusAnchorId}
          />
        </section>

        <section className="graph-panel" aria-label="Interactive discourse graph">
          <div className="graph-legend">
            <span><i className="legend-author" /> authorial</span>
            <span><i className="legend-inferred" /> inferred</span>
            <span>Click paragraphs to trace evidence</span>
          </div>
          <ReactFlow
            nodes={flowNodes}
            edges={flowEdges}
            nodeTypes={nodeTypes}
            nodesDraggable={false}
            nodesConnectable={false}
            elementsSelectable
            minZoom={0.12}
            maxZoom={1.8}
            onNodeClick={(_, node) => { setSelection({ kind: 'node', id: node.id }); setFocusAnchorId(node.data.anchor_ids?.[0] ?? null); }}
            onEdgeClick={(_, edge) => { const id = edge.data?.edgeId; if (id) { setSelection({ kind: 'edge', id }); const original = document.edges.find((item) => item.id === id); setFocusAnchorId(original?.evidence_anchor_ids?.[0] ?? null); } }}
            fitView
          >
            <Background gap={22} size={1} />
            <MiniMap pannable zoomable />
            <Controls showInteractive={false} />
          </ReactFlow>
        </section>

        <aside className="panel inspector-panel">
          <div className="panel-heading"><div><span className="eyebrow">Reconstruction</span><h1>Inspector</h1></div></div>
          <Inspector document={document} selection={selection} onDocumentChange={setDocument} onFocusAnchor={setFocusAnchorId} />
        </aside>
      </main>
    </div>
  );
}

export default function App() {
  return <ReactFlowProvider><AppInner /></ReactFlowProvider>;
}
