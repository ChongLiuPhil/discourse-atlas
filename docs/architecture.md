# Architecture

## Canonical model

Discourse Atlas separates **hierarchy** from **dependency**.

A node's `parent_id` records containment. Directed edges record discourse relations. JSON Schema validates shape; a second semantic-validation pass checks graph invariants such as unique IDs, valid references, one work root, and an acyclic containment hierarchy. This permits:

- nested boxes in a visualization;
- arrows among siblings;
- arrows across chapters or levels;
- cyclic dependency interpretations where a text genuinely revisits and mutually determines concepts.

## Why JSON is canonical

The model should remain independent of any visualization library. React Flow, ELK, Mermaid, Graphviz, or future renderers can all consume the same graph.

## Long-text strategy

Long works should be analyzed recursively:

1. recover top-level structure;
2. analyze leaf units within one parent;
3. infer sibling relations;
4. synthesize the parent;
5. repeat upward;
6. search for cross-hierarchy relations;
7. audit evidence and uncertainty.

This avoids asking a model to hold an entire book-level dependency graph in one undifferentiated pass.

## Future interactive viewer

Recommended pipeline:

```text
source text
   ↓
agent + discourse-structure skill
   ↓
discourse graph JSON
   ↓
schema validator
   ↓
ELK layout
   ↓
React Flow interactive graph
```

The viewer should provide at least three zoom levels: work, chapter/part, and local argument map. Important edges should expose their explanation, evidence anchors, confidence, and assertion level.
