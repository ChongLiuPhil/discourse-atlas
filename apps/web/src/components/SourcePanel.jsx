import { useEffect, useMemo } from 'react';
import { sourceBlocksFromText } from '../model.js';

export default function SourcePanel({ source, anchors, activeAnchorIds, focusAnchorId, onAnchorFocus }) {
  const blocks = useMemo(() => sourceBlocksFromText(source), [source]);
  const paragraphToAnchors = useMemo(() => {
    const map = new Map();
    for (const anchor of anchors) {
      if (anchor.paragraph_start) {
        const end = anchor.paragraph_end ?? anchor.paragraph_start;
        for (let paragraph = anchor.paragraph_start; paragraph <= end; paragraph += 1) {
          const ids = map.get(paragraph) ?? [];
          ids.push(anchor.id);
          map.set(paragraph, ids);
        }
        continue;
      }
      if (anchor.line_start) {
        const lineEnd = anchor.line_end ?? anchor.line_start;
        blocks.forEach((block, index) => {
          if (block.lineStart <= lineEnd && block.lineEnd >= anchor.line_start) {
            const paragraph = index + 1;
            const ids = map.get(paragraph) ?? [];
            ids.push(anchor.id);
            map.set(paragraph, ids);
          }
        });
      }
    }
    return map;
  }, [anchors, blocks]);

  useEffect(() => {
    if (!focusAnchorId) return;
    const anchor = anchors.find((item) => item.id === focusAnchorId);
    let paragraph = anchor?.paragraph_start ?? null;
    if (!paragraph && anchor?.line_start) {
      const index = blocks.findIndex((block) => block.lineStart <= anchor.line_start && block.lineEnd >= anchor.line_start);
      if (index >= 0) paragraph = index + 1;
    }
    if (!paragraph) return;
    document.getElementById(`source-paragraph-${paragraph}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [focusAnchorId, anchors, blocks]);

  if (!source.trim()) {
    return <div className="empty-state">Load a Markdown or text source to synchronize evidence with the graph.</div>;
  }

  return (
    <div className="source-document">
      {blocks.map((block, index) => {
        const number = index + 1;
        const anchorIds = paragraphToAnchors.get(number) ?? [];
        const active = anchorIds.some((id) => activeAnchorIds.has(id));
        return (
          <article
            id={`source-paragraph-${number}`}
            key={number}
            className={`source-paragraph ${active ? 'is-active' : ''}`}
            onClick={() => anchorIds[0] && onAnchorFocus(anchorIds[0])}
          >
            <div className="paragraph-number">¶{number}</div>
            <p>{block.text.replace(/\s+/g, ' ')}</p>
            <div className="line-range">lines {block.lineStart}–{block.lineEnd}</div>
            {anchorIds.length ? <div className="anchor-list">{anchorIds.join(' · ')}</div> : null}
          </article>
        );
      })}
    </div>
  );
}
