# Discourse Atlas Benchmark Protocol

The benchmark tests whether a reconstruction is **structurally faithful and evidence-grounded**, without pretending that every argumentative text has exactly one uniquely correct graph.

## Three evaluation modes

### 1. Stable-ID gold comparison

```bash
discourse-atlas evaluate benchmark/cases/mini-essay/gold.json candidate.json
```

Use this when reference and candidate already share unit IDs.

### 2. Explicit unit alignment

```bash
discourse-atlas align reference.json candidate.json -o proposed-alignment.json
discourse-atlas evaluate reference.json candidate.json --alignment reviewed-alignment.json
```

Alignment is a separate inspectable artifact. It may map one or several nodes on either side into a shared unit, so split/merge segmentation differences do not have to be mistaken for relation errors. Automatic proposals use deterministic source-anchor overlap and are marked as proposals rather than silently accepted semantic matches.

### 3. Multi-reference scoring

```bash
discourse-atlas multi-evaluate candidate.json ref-a.json ref-b.json --auto-align
```

The report contains all per-reference scores, `best_reference`, `best_macro_score`, mean score, and score range. Do not collapse several defensible interpretations into a synthetic averaged graph.

## Metrics after alignment

- aligned-unit coverage (precision / recall / F1);
- parent/hierarchy accuracy;
- authorial-vs-inferred structure-origin accuracy;
- relation edge precision / recall / F1;
- node evidence grounding by source coordinates;
- edge evidence grounding by source coordinates;
- unweighted macro score for regression tracking.

The macro score is a convenience regression signal, **not** a claim that these dimensions have equal philosophical importance.

## Inter-annotation agreement

```bash
discourse-atlas agreement annotation-a.json annotation-b.json
discourse-atlas agreement reference-a.json reference-b.json --alignment alignment-a-b.json
```

Agreement is symmetric. Disagreement is retained as data rather than automatically resolved into a single graph.

## Case requirements

Each benchmark case should include:

- redistributable or project-authored source text;
- provenance/license note;
- stable source anchors;
- one or more reviewed graph annotations;
- short adjudication notes identifying genuine ambiguity;
- explicit distinction between authorial headings and inferred structure.

## Current corpus

`manifest.json` contains four project-authored synthetic regression cases plus one public-domain philosophical case from John Stuart Mill's *On Liberty*. The Mill case includes two accepted references and a reviewed split/merge alignment.

Future additions should expand public-domain or permission-compatible real texts and should use multiple annotators where feasible.
