import { useEffect, useMemo } from 'react';
import { anchorLocationLabel, blockNumbersForAnchor, sourceBlocksFromText } from '../model.js';

export default function SourcePanel({ source, anchors, activeAnchorIds, focusAnchorId, onAnchorFocus }) {
  const blocks = useMemo(() => sourceBlocksFromText(source), [source]);
  const blockToAnchors = useMemo(() => {
    const map = new Map();
    for (const anchor of anchors) {
      for (const blockNumber of blockNumbersForAnchor(anchor, blocks)) {
        const ids = map.get(blockNumber) ?? [];
        ids.push(anchor.id);
        map.set(blockNumber, ids);
      }
    }
    return map;
  }, [anchors, blocks]);

  useEffect(() => {
    if (!focusAnchorId) return;
    const anchor = anchors.find((item) => item.id === focusAnchorId);
    const [blockNumber] = blockNumbersForAnchor(anchor, blocks);
    if (!blockNumber) return;
    document.getElementById(`source-paragraph-${blockNumber}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [focusAnchorId, anchors, blocks]);

  if (!source.trim()) {
    return <div className="empty-state">Load a Markdown or text source to synchronize evidence with the graph.</div>;
  }

  return (
    <div className="source-document">
      {blocks.map((block, index) => {
        const number = index + 1;
        const anchorIds = blockToAnchors.get(number) ?? [];
        const active = anchorIds.some((id) => activeAnchorIds.has(id));
        const anchorLabels = anchorIds.map((id) => {
          const anchor = anchors.find((item) => item.id === id);
          const location = anchorLocationLabel(anchor);
          return location ? `${id} (${location})` : id;
        });
        return (
          <article
            id={`source-paragraph-${number}`}
            key={number}
            className={`source-paragraph ${active ? 'is-active' : ''}`}
            onClick={() => anchorIds[0] && onAnchorFocus(anchorIds[0])}
          >
            <div className="paragraph-number">¶{number}</div>
            <p>{block.text.replace(/\s+/g, ' ')}</p>
            <div className="line-range">
              lines {block.lineStart}–{block.lineEnd} · chars {block.charStart}–{block.charEnd}
              {block.pageStart ? ` · page ${block.pageStart}${block.pageEnd !== block.pageStart ? `–${block.pageEnd}` : ''}` : ''}
            </div>
            {anchorLabels.length ? <div className="anchor-list">{anchorLabels.join(' · ')}</div> : null}
          </article>
        );
      })}
    </div>
  );
}
