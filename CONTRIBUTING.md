# Contributing to Discourse Atlas

Discourse Atlas is specification-first. Changes to the ontology or schema can affect every downstream analysis, so please keep proposals explicit and testable.

## Good first contributions

- Add a small, legally redistributable example text and a hand-reviewed analysis.
- Improve relation definitions and counterexamples.
- Add schema validation tests.
- Improve Mermaid / DOT exports.
- Propose evaluation criteria for structural fidelity.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
```

## Ontology changes

For a new relation type, explain:

1. what it means;
2. edge direction;
3. how it differs from existing relations;
4. at least one positive example;
5. at least one tempting false positive.

Prefer a small stable ontology over a large ambiguous one.

## Pull requests

Keep PRs focused. Schema changes should update:

- `schemas/discourse-graph.schema.json`
- `skills/discourse-structure/references/relation-ontology.md` when relevant
- examples/tests that demonstrate the change
