# Relation ontology review — v0.4 decision record

The initial nine-relation ontology was reviewed against the interactive reader and evaluation requirements. The decision for v0.4 is to **keep the ontology small and unchanged** rather than add relations before benchmark evidence justifies them.

## Decisions

- `requires`, `supports`, `derives`, `refines`, `objects_to`, `responds_to`, `illustrates`, and `sequence` remain directed.
- `contrasts` is semantically symmetric. It is stored once using the existing edge shape; renderers should not imply a substantive causal direction from the stored endpoint order.
- `sequence` remains explicitly non-logical. It records organization/order only and must not be counted as evidence that the target logically depends on the source.
- Problem/answer, motivation, definition-use, synthesis, and similar discourse roles remain **node functions / roles** for now. Adding them as edge types would duplicate node-role information without enough benchmark evidence that a distinct dependency relation is needed.
- Confidence and `assertion_level` remain separate: confidence is graded uncertainty; assertion level records whether the relation is explicit, strongly inferred, or tentative.
- Competing reconstructions are represented as separate complete graph documents for v0.4. A future schema may add a lightweight alternatives layer, but only after evaluation work shows a stable requirement.

## Deferred schema questions

Page and character offsets are useful for PDFs and richer source formats, but the v0.4 reader already supports paragraph and line anchors. Adding coordinates is deferred to a schema version bump so current `0.1.0` graphs remain valid without migration.

Renderer metadata remains non-canonical. Positions, collapse state, viewport state, and visual styling must not enter the discourse graph schema.

## Change criterion

A new relation type should be added only when we can provide:

1. a directionality rule;
2. positive examples;
3. common false positives;
4. evidence that existing relations/node roles cannot express the distinction cleanly;
5. migration/evaluation impact.
