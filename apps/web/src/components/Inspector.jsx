import { useEffect, useMemo, useState } from 'react';
import { anchorLocationLabel, RELATIONS } from '../model.js';

function Confidence({ value }) {
  return <span className="confidence-chip">{Math.round(value * 100)}%</span>;
}

export default function Inspector({ document, selection, onDocumentChange, onFocusAnchor }) {
  const selected = useMemo(() => {
    if (!selection) return null;
    const collection = selection.kind === 'node' ? document.nodes : document.edges;
    return collection.find((item) => item.id === selection.id) ?? null;
  }, [document, selection]);
  const [draft, setDraft] = useState(selected);

  useEffect(() => setDraft(selected), [selected]);

  if (!selected || !selection || !draft) {
    return <div className="empty-state">Select a node or relation to inspect its role, evidence, confidence, and edit the reconstruction.</div>;
  }

  const isNode = selection.kind === 'node';
  const anchorIds = isNode ? selected.anchor_ids : selected.evidence_anchor_ids;

  function update(field, value) {
    setDraft((current) => ({ ...current, [field]: value }));
  }

  function save() {
    const key = isNode ? 'nodes' : 'edges';
    onDocumentChange({
      ...document,
      [key]: document[key].map((item) => item.id === draft.id ? draft : item),
    });
  }

  return (
    <div className="inspector">
      <div className="inspector-kicker">{isNode ? `${selected.kind} node` : `${selected.relation} relation`}</div>
      <h2>{isNode ? selected.title : `${selected.source} → ${selected.target}`}</h2>
      <div className="inspector-meta">
        <Confidence value={selected.confidence} />
        {!isNode ? <span>{selected.assertion_level.replaceAll('_', ' ')}</span> : <span>{selected.structure_origin} structure</span>}
      </div>

      {isNode ? (
        <>
          <label>Title<input value={draft.title} onChange={(e) => update('title', e.target.value)} /></label>
          <label>Summary<textarea rows="4" value={draft.summary} onChange={(e) => update('summary', e.target.value)} /></label>
          <label>Role in parent<textarea rows="3" value={draft.role_in_parent ?? ''} onChange={(e) => update('role_in_parent', e.target.value || null)} /></label>
          <label>Structure origin<select value={draft.structure_origin} onChange={(e) => update('structure_origin', e.target.value)}><option value="author">author</option><option value="inferred">inferred</option></select></label>
        </>
      ) : (
        <>
          <label>Relation<select value={draft.relation} onChange={(e) => update('relation', e.target.value)}>{RELATIONS.map((relation) => <option key={relation}>{relation}</option>)}</select></label>
          <label>Explanation<textarea rows="5" value={draft.explanation} onChange={(e) => update('explanation', e.target.value)} /></label>
          <label>Assertion level<select value={draft.assertion_level} onChange={(e) => update('assertion_level', e.target.value)}><option value="explicit">explicit</option><option value="strongly_inferred">strongly inferred</option><option value="tentative">tentative</option></select></label>
          <label>Confidence<input type="range" min="0" max="1" step="0.01" value={draft.confidence} onChange={(e) => update('confidence', Number(e.target.value))} /><span>{draft.confidence.toFixed(2)}</span></label>
        </>
      )}

      <div className="evidence-section">
        <div className="section-label">Source anchors</div>
        <div className="evidence-buttons">
          {anchorIds.length ? anchorIds.map((id) => {
            const anchor = document.anchors.find((item) => item.id === id);
            const location = anchorLocationLabel(anchor);
            return <button key={id} onClick={() => onFocusAnchor(id)}>{id}{location ? ` · ${location}` : ''}</button>;
          }) : <span>No anchors</span>}
        </div>
      </div>
      {!isNode && selected.notes ? <div className="inspector-note">{selected.notes}</div> : null}
      <button className="primary-button" onClick={save}>Save correction</button>
    </div>
  );
}
