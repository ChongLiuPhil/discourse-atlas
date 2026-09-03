# Evaluation philosophy

Discourse Atlas treats structural reconstruction as a constrained interpretive task. Some errors are objective (invented source anchors, broken containment, missing endpoints); other disagreements can reflect legitimate readings.

For that reason, evaluation is layered:

1. **Validity** — schema and graph invariants.
2. **Segmentation/alignment** — whether compared annotations refer to the same textual units.
3. **Hierarchy fidelity** — parent relations and authorial/inferred status.
4. **Relation fidelity** — typed dependencies among aligned units.
5. **Evidence grounding** — whether nodes and relation claims point to the same source anchors.
6. **Agreement analysis** — whether multiple annotators converge, without forcing adjudication where disagreement is defensible.

The CLI's exact-ID metrics cover layers 3–5 after alignment. Future research can add semantic alignment and calibrated uncertainty, but those should remain separately inspectable stages.
