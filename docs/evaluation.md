# Evaluation philosophy

Discourse Atlas treats structural reconstruction as a constrained interpretive task. Some errors are objective (invented source anchors, broken containment, missing endpoints); other disagreements can reflect legitimate readings.

Evaluation is layered:

1. **Validity** — schema and graph invariants.
2. **Segmentation/alignment** — whether compared annotations refer to the same textual units.
3. **Hierarchy fidelity** — parent relations and authorial/inferred status.
4. **Relation fidelity** — typed dependencies among aligned units.
5. **Evidence grounding** — whether nodes and relation claims point to the same source material.
6. **Reference plurality** — whether a candidate matches one among several accepted reconstructions.
7. **Agreement analysis** — whether annotators converge, without forcing adjudication where disagreement is defensible.

## Stable-ID mode

If node IDs are already shared, `evaluate` uses exact IDs and reports hierarchy accuracy, relation precision/recall/F1, node-anchor grounding, edge-evidence grounding, and an unweighted macro score.

## Explicit-alignment mode

If IDs or segmentation differ, provide an alignment JSON. Aligned nodes are collapsed into common units before structural scoring. Evidence is compared by source coordinates rather than anchor identifier strings. See `docs/alignment.md`.

## Multi-reference mode

`multi-evaluate` preserves several accepted references and reports the best-reference score plus the full per-reference distribution. The best score is useful for testing compatibility with defensible readings; the distribution preserves interpretive sensitivity.

No macro score should be interpreted as a measure of philosophical truth. It is a regression and comparison instrument whose components remain inspectable.
