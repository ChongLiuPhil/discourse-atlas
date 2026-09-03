# Discourse Atlas Benchmark Protocol

The benchmark tests whether a reconstruction is **structurally faithful and evidence-grounded**, without pretending that every argumentative text has exactly one uniquely correct graph.

## Two evaluation modes

### 1. Gold comparison

Use this when a case has a reviewed reference reconstruction with stable node IDs:

```bash
discourse-atlas evaluate benchmark/cases/mini-essay/gold.json candidate.json
```

Reported metrics:

- node-ID coverage (precision / recall / F1);
- parent/hierarchy accuracy on aligned non-root nodes;
- authorial-vs-inferred structure-origin accuracy;
- relation edge precision / recall / F1 on `(source, target, relation)`;
- node-anchor precision / recall / F1;
- edge-evidence-anchor precision / recall / F1;
- an unweighted macro score for regression tracking.

The macro score is a convenience regression signal, **not** a claim that these dimensions have equal philosophical importance.

### 2. Inter-annotator agreement

Use this for two independently reviewed reconstructions that share stable node IDs:

```bash
discourse-atlas agreement annotation-a.json annotation-b.json
```

This reports symmetric Jaccard/accuracy measures. Disagreement is retained as data rather than automatically resolved into a single graph.

## Stable IDs and alignment

The initial metrics deliberately do not perform fuzzy semantic node matching. Benchmark cases should assign stable unit IDs before independent relation annotation, or researchers should create an explicit alignment file/process first. Automatic embedding-based alignment would otherwise mix **segmentation/alignment errors** with **structural reasoning errors**.

For unconstrained model outputs, evaluation should therefore occur in two stages:

1. segmentation/unit alignment;
2. hierarchy, relation, and evidence evaluation on the aligned units.

## Multiple defensible reconstructions

A benchmark case may contain more than one reviewed reference graph. A candidate can be scored against each accepted reference and reported with both:

- best-reference score;
- score distribution across references.

Do not silently collapse interpretive disagreement into a single averaged graph.

## Case requirements

Each benchmark case should include:

- redistributable or project-authored source text;
- provenance/license note;
- stable source anchors;
- one or more reviewed graph annotations;
- short adjudication notes identifying genuine ambiguity;
- explicit distinction between authorial headings and inferred structure.

## Current corpus

`manifest.json` currently lists four project-authored synthetic cases spanning a general essay, a philosophical argument, academic methodology, and policy reasoning. They are intended as a small cross-genre regression corpus, not as a representative estimate of humanities-model performance.

Future benchmark additions should prefer public-domain or permission-compatible real texts and should be reviewed by at least two annotators where feasible.
