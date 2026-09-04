import { useEffect, useMemo, useState } from 'react';
import {
  addReviewedUnit,
  alignmentCoverage,
  indexNodes,
  mappedNodeIds,
  proposeAlignment,
  refreshUnmatched,
  removeUnit,
  updateUnit,
  validateWorkbenchAlignment,
} from '../alignmentModel.js';

function NodeCard({ node, side, selected, mapped, onToggle }) {
  if (!node) return null;
  return (
    <label className={`alignment-node-card ${selected ? 'selected' : ''} ${mapped ? 'mapped' : ''}`}>
      <input type="checkbox" checked={selected} disabled={mapped} onChange={() => onToggle(node.id)} />
      <div className="alignment-node-copy">
        <div className="alignment-node-meta"><span>{side}</span><span>{node.kind}</span><span>{node.structure_origin ?? 'unknown'}</span></div>
        <strong>{node.title || node.id}</strong>
        <small>{node.id}</small>
        {node.summary ? <p>{node.summary}</p> : null}
        <div className="anchor-chips">{(node.anchor_ids ?? []).map((id) => <span key={id}>{id}</span>)}</div>
      </div>
    </label>
  );
}

function UnitCard({ unit, referenceIndex, candidateIndex, onStatus, onRemove }) {
  const titleFor = (index, id) => index.get(id)?.title ?? id;
  return (
    <article className={`alignment-unit-card status-${unit.status ?? 'proposed'}`}>
      <div className="alignment-unit-head">
        <div><strong>{unit.unit_id}</strong><span>{unit.method ?? 'manual'} · {Math.round((unit.confidence ?? 1) * 100)}%</span></div>
        <button className="quiet-button" onClick={() => onRemove(unit.unit_id)}>Remove</button>
      </div>
      <div className="alignment-unit-pair">
        <div><span className="eyebrow">Reference</span>{(unit.reference_node_ids ?? []).map((id) => <p key={id}>{titleFor(referenceIndex, id)} <small>{id}</small></p>)}</div>
        <div className="alignment-arrow">↔</div>
        <div><span className="eyebrow">Candidate</span>{(unit.candidate_node_ids ?? []).map((id) => <p key={id}>{titleFor(candidateIndex, id)} <small>{id}</small></p>)}</div>
      </div>
      {unit.rationale ? <p className="alignment-rationale">{unit.rationale}</p> : null}
      <div className="alignment-actions">
        <button className={unit.status === 'accepted' ? 'active' : ''} onClick={() => onStatus(unit.unit_id, 'accepted')}>Accept</button>
        <button className={unit.status === 'proposed' ? 'active' : ''} onClick={() => onStatus(unit.unit_id, 'proposed')}>Proposed</button>
        <button className={unit.status === 'rejected' ? 'active danger' : ''} onClick={() => onStatus(unit.unit_id, 'rejected')}>Reject</button>
      </div>
    </article>
  );
}

export default function AlignmentWorkbench({ onBack }) {
  const [reference, setReference] = useState(null);
  const [candidate, setCandidate] = useState(null);
  const [alignment, setAlignment] = useState({ alignment_version: '0.1.0', method: 'manual-reviewed', units: [] });
  const [selectedReference, setSelectedReference] = useState(new Set());
  const [selectedCandidate, setSelectedCandidate] = useState(new Set());
  const [rationale, setRationale] = useState('');
  const [threshold, setThreshold] = useState(0.5);
  const [status, setStatus] = useState('Loading reviewed Mill example…');

  const referenceIndex = useMemo(() => indexNodes(reference), [reference]);
  const candidateIndex = useMemo(() => indexNodes(candidate), [candidate]);
  const referenceMapped = useMemo(() => mappedNodeIds(alignment, 'reference'), [alignment]);
  const candidateMapped = useMemo(() => mappedNodeIds(alignment, 'candidate'), [alignment]);
  const coverage = useMemo(() => alignmentCoverage(reference, candidate, alignment), [reference, candidate, alignment]);
  const errors = useMemo(() => reference && candidate ? validateWorkbenchAlignment(reference, candidate, alignment) : [], [reference, candidate, alignment]);

  useEffect(() => {
    Promise.all([
      fetch('./mill-reference-a.json').then((response) => response.json()),
      fetch('./mill-reference-b.json').then((response) => response.json()),
      fetch('./mill-alignment-a-b.json').then((response) => response.json()),
    ]).then(([ref, cand, reviewed]) => {
      setReference(ref);
      setCandidate(cand);
      setAlignment(refreshUnmatched(ref, cand, reviewed));
      setStatus('Reviewed split/merge example loaded');
    }).catch((error) => setStatus(`Could not load alignment example: ${error}`));
  }, []);

  function toggle(setter, id) {
    setter((current) => {
      const next = new Set(current);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  function setNextAlignment(next) {
    setAlignment(reference && candidate ? refreshUnmatched(reference, candidate, next) : next);
  }

  function generateProposal() {
    if (!reference || !candidate) return;
    try {
      setNextAlignment(proposeAlignment(reference, candidate, threshold));
      setSelectedReference(new Set());
      setSelectedCandidate(new Set());
      setStatus('Fresh deterministic proposal generated. Review before export.');
    } catch (error) {
      setStatus(String(error));
    }
  }

  function addManualUnit() {
    try {
      const next = addReviewedUnit(alignment, [...selectedReference], [...selectedCandidate], rationale.trim());
      setNextAlignment(next);
      setSelectedReference(new Set());
      setSelectedCandidate(new Set());
      setRationale('');
      setStatus('Reviewed unit added');
    } catch (error) {
      setStatus(String(error));
    }
  }

  function changeStatus(unitId, nextStatus) {
    setNextAlignment(updateUnit(alignment, unitId, { status: nextStatus }));
  }

  function acceptStrongProposals() {
    const next = { ...alignment, units: (alignment.units ?? []).map((unit) => unit.status === 'proposed' && (unit.confidence ?? 0) >= 0.9 ? { ...unit, status: 'accepted' } : unit) };
    setNextAlignment(next);
    setStatus('Accepted proposals with confidence ≥ 0.90; lower-confidence units remain proposed');
  }

  async function uploadJson(event, setter, label) {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const parsed = JSON.parse(await file.text());
      setter(parsed);
      setStatus(`${label} loaded: ${file.name}`);
    } catch (error) {
      setStatus(`Invalid ${label} JSON: ${error}`);
    } finally {
      event.target.value = '';
    }
  }

  async function uploadAlignment(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const parsed = JSON.parse(await file.text());
      setNextAlignment(parsed);
      setStatus(`Alignment loaded: ${file.name}`);
    } catch (error) {
      setStatus(`Invalid alignment JSON: ${error}`);
    } finally {
      event.target.value = '';
    }
  }

  function exportAlignment() {
    if (errors.length) {
      setStatus('Resolve alignment errors before export');
      return;
    }
    const reviewed = refreshUnmatched(reference, candidate, { ...alignment, method: 'manual-reviewed' });
    const blob = new Blob([`${JSON.stringify(reviewed, null, 2)}\n`], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = Object.assign(window.document.createElement('a'), { href: url, download: 'alignment.reviewed.json' });
    link.click();
    URL.revokeObjectURL(url);
  }

  if (!reference || !candidate) {
    return <main className="loading-screen"><h1>Alignment workbench</h1><p>{status}</p><button onClick={onBack}>Back to reader</button></main>;
  }

  return (
    <div className="alignment-shell">
      <header className="topbar">
        <div className="brand"><div className="brand-mark">DA</div><div><strong>Alignment workbench</strong><span>Review textual-unit correspondence before scoring</span></div></div>
        <div className="toolbar">
          <span className="status">{status}</span>
          <button onClick={onBack}>Reader</button>
          <label className="file-button">Reference<input type="file" accept="application/json,.json" onChange={(event) => uploadJson(event, setReference, 'reference')} /></label>
          <label className="file-button">Candidate<input type="file" accept="application/json,.json" onChange={(event) => uploadJson(event, setCandidate, 'candidate')} /></label>
          <label className="file-button">Alignment<input type="file" accept="application/json,.json" onChange={uploadAlignment} /></label>
          <button onClick={exportAlignment} disabled={errors.length > 0}>Export reviewed</button>
        </div>
      </header>

      <div className="alignment-metrics">
        <div><span>Reference mapped</span><strong>{coverage.referenceMapped}/{coverage.referenceTotal}</strong><progress value={coverage.referenceRatio} max="1" /></div>
        <div><span>Candidate mapped</span><strong>{coverage.candidateMapped}/{coverage.candidateTotal}</strong><progress value={coverage.candidateRatio} max="1" /></div>
        <div><span>Active units</span><strong>{(alignment.units ?? []).filter((unit) => unit.status !== 'rejected').length}</strong><small>{errors.length ? `${errors.length} validation issue(s)` : 'valid membership'}</small></div>
        <div className="proposal-controls"><label>Anchor threshold <input type="number" min="0" max="1" step="0.05" value={threshold} onChange={(event) => setThreshold(Number(event.target.value))} /></label><button onClick={generateProposal}>Generate proposal</button><button onClick={acceptStrongProposals}>Accept ≥ 0.90</button></div>
      </div>

      {errors.length ? <div className="error-banner">{errors.join(' · ')}</div> : null}

      <main className="alignment-workspace">
        <section className="alignment-side">
          <div className="alignment-side-heading"><span className="eyebrow">Reference reconstruction</span><h2>{reference.document?.title}</h2><small>{alignment.unmatched_reference_node_ids?.length ?? 0} unmatched</small></div>
          <div className="alignment-node-list">{reference.nodes.map((node) => <NodeCard key={node.id} node={node} side="REF" selected={selectedReference.has(node.id)} mapped={referenceMapped.has(node.id)} onToggle={(id) => toggle(setSelectedReference, id)} />)}</div>
        </section>

        <section className="alignment-center">
          <div className="manual-unit-builder">
            <span className="eyebrow">Manual reviewed unit</span>
            <strong>{selectedReference.size} reference ↔ {selectedCandidate.size} candidate</strong>
            <textarea placeholder="Rationale for this correspondence (recommended for split/merge units)" value={rationale} onChange={(event) => setRationale(event.target.value)} />
            <button onClick={addManualUnit} disabled={!selectedReference.size || !selectedCandidate.size}>Create accepted unit</button>
          </div>
          <div className="alignment-unit-list">{(alignment.units ?? []).map((unit) => <UnitCard key={unit.unit_id} unit={unit} referenceIndex={referenceIndex} candidateIndex={candidateIndex} onStatus={changeStatus} onRemove={(id) => setNextAlignment(removeUnit(alignment, id))} />)}</div>
        </section>

        <section className="alignment-side">
          <div className="alignment-side-heading"><span className="eyebrow">Candidate reconstruction</span><h2>{candidate.document?.title}</h2><small>{alignment.unmatched_candidate_node_ids?.length ?? 0} unmatched</small></div>
          <div className="alignment-node-list">{candidate.nodes.map((node) => <NodeCard key={node.id} node={node} side="CAND" selected={selectedCandidate.has(node.id)} mapped={candidateMapped.has(node.id)} onToggle={(id) => toggle(setSelectedCandidate, id)} />)}</div>
        </section>
      </main>
    </div>
  );
}
