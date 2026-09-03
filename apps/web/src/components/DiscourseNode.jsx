import { Handle, Position } from '@xyflow/react';

function OriginBadge({ origin }) {
  return <span className={`origin-badge origin-${origin}`}>{origin === 'author' ? 'authorial' : 'AI inferred'}</span>;
}

export function DiscourseNode({ data, selected }) {
  return (
    <div className={`discourse-node ${selected ? 'is-selected' : ''} ${data.dimmed ? 'is-dimmed' : ''} ${data.highlighted ? 'is-highlighted' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div className="node-heading">
        <span className="node-kind">{data.kind}</span>
        <OriginBadge origin={data.structure_origin} />
      </div>
      <div className="node-title">{data.title}</div>
      <div className="node-summary">{data.summary}</div>
      <div className="node-footer">
        <span>{Math.round(data.confidence * 100)}% confidence</span>
        {data.collapsible ? (
          <button className="node-button nodrag" onClick={(event) => { event.stopPropagation(); data.onToggleCollapse(data.id); }}>
            {data.collapsed ? `Expand (${data.hiddenCount})` : 'Collapse'}
          </button>
        ) : null}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export function ContainerNode({ data, selected }) {
  return (
    <div className={`container-node ${selected ? 'is-selected' : ''} ${data.dimmed ? 'is-dimmed' : ''} ${data.highlighted ? 'is-highlighted' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div className="container-heading">
        <div>
          <div className="node-kind">{data.kind}</div>
          <div className="container-title">{data.title}</div>
        </div>
        <div className="container-actions">
          <OriginBadge origin={data.structure_origin} />
          <button className="node-button nodrag" onClick={(event) => { event.stopPropagation(); data.onToggleCollapse(data.id); }}>Collapse</button>
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
