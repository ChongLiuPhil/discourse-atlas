# Discourse Atlas

[![CI](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml)

**Discourse Atlas** is an open-source, agent-skill-first toolkit for reconstructing the hierarchical structure and logical dependencies of argumentative and expository texts.

It is designed for essays, philosophy, academic papers, theoretical books, legal reasoning, policy reports, and other texts where understanding **how the parts depend on one another** matters as much as understanding what each part says.

> Status: **v0.5.0 research preview.** The toolkit now includes explicit split/merge-capable unit alignment, multi-reference evaluation, and a public-domain philosophy benchmark in addition to the analysis skill, graph format, validator/exporters, interactive reader, and evaluation toolkit.

## Core idea

Discourse Atlas models a text as two related structures:

1. **Containment hierarchy** — work → part → chapter → section → paragraph / argument unit.
2. **Discourse dependency graph** — relations such as `requires`, `supports`, `derives`, `refines`, `objects_to`, and `responds_to`.

The canonical representation is JSON. Visualizations are derived views, not the source of truth.

## Design principles

- **Structure before summary.** Recover the architecture of the text before summarizing it.
- **Preserve authorial structure.** If the author provides chapters or sections, retain them.
- **Mark inferred structure explicitly.** AI-generated sections must never be presented as authorial headings.
- **Separate hierarchy from dependency.** Containment is not the same as logical dependence.
- **Evidence for important edges.** Major inferred relations should point back to source anchors.
- **Alignment before comparison.** Different node IDs or segmentation must be aligned explicitly before structural differences are scored.
- **Reconstruction, not revelation.** The output is a criticizable interpretation, not a claim to the single true structure of a text.

## Repository layout

```text
discourse-atlas/
├── skills/discourse-structure/   # Portable Agent Skill
├── schemas/                      # Graph + unit-alignment schemas
├── src/discourse_atlas/          # Validation, alignment, export, evaluation CLI
├── apps/web/                     # Interactive React Flow + ELK reader
├── examples/mini-essay/          # Small end-to-end example
├── benchmark/                    # Synthetic + public-domain evaluation cases
├── tests/                        # Schema, renderer, alignment, evaluation tests
├── docs/                         # Architecture, ontology, alignment, evaluation notes
└── .github/workflows/            # CI
```

## Use as an Agent Skill

Copy `skills/discourse-structure/` into a client that supports the Agent Skills `SKILL.md` format. Ask the agent to analyze a text's discourse structure and produce `analysis.json` and `analysis.md`. The skill is intentionally model- and vendor-neutral.

## CLI

```bash
python -m pip install -e '.[dev]'

discourse-atlas validate examples/mini-essay/analysis.json
discourse-atlas mermaid examples/mini-essay/analysis.json
discourse-atlas dot examples/mini-essay/analysis.json

# Stable-ID evaluation
discourse-atlas evaluate reference.json candidate.json

# Propose and review unit alignment
discourse-atlas align reference.json candidate.json -o alignment.json
discourse-atlas evaluate reference.json candidate.json --alignment alignment.json

# Preserve several defensible references
discourse-atlas multi-evaluate candidate.json ref-a.json ref-b.json --auto-align

# Symmetric annotation agreement
discourse-atlas agreement ref-a.json ref-b.json --alignment alignment.json
```

Validation checks JSON shape plus unique IDs, parent references, containment cycles, edge endpoints, evidence anchors, and anchor ranges. Alignment validation checks unknown nodes, duplicate membership, and ambiguous repeated mappings.

## Interactive reader

The web app in `apps/web/` turns the canonical graph into a synchronized reading environment with nested React Flow nodes and ELK layout.

```bash
cd apps/web
npm install
npm run dev
```

It supports collapse/expand, source ↔ graph evidence tracing, paragraph and line anchors, node/edge inspection, human correction, local file loading, and corrected-JSON export.

## Relation ontology (MVP)

| Relation | Meaning |
|---|---|
| `requires` | source is a prerequisite for understanding or establishing target |
| `supports` | source gives reasons/evidence for target |
| `derives` | target is developed or derived from source |
| `refines` | source makes target more precise, qualified, restricted, or articulated |
| `contrasts` | source and target are deliberately contrasted (semantically symmetric) |
| `objects_to` | source raises an objection to target |
| `responds_to` | source answers a problem or objection in target |
| `illustrates` | source exemplifies or applies target |
| `sequence` | textual/organizational order only; not logical dependence |

See `skills/discourse-structure/references/relation-ontology.md` and `docs/ontology-review-v0.4.md`.

## Completed milestones

### v0.1 — specification-first MVP
- [x] Portable `SKILL.md`
- [x] JSON Schema
- [x] Relation ontology and segmentation rules
- [x] Validator + Mermaid/DOT exporters

### v0.2 — interactive map
- [x] React Flow viewer
- [x] ELK compound/hierarchical layout
- [x] Collapsible nested sections
- [x] Edge evidence inspector

### v0.3 — synchronized reading
- [x] Source text + map side-by-side
- [x] Graph → source navigation
- [x] Source → graph highlighting
- [x] Human correction workflow + JSON export

### v0.4 — evaluation
- [x] Benchmark protocol + four-case cross-genre synthetic corpus
- [x] Inter-annotation comparison command
- [x] Structural fidelity metrics
- [x] Relation and evidence precision / recall metrics

### v0.5 — alignment and interpretive plurality
- [x] Explicit one-to-one / split / merge unit-alignment format
- [x] Deterministic source-anchor alignment proposals
- [x] Alignment-aware hierarchy/relation/evidence scoring
- [x] Multi-reference scoring with best/mean/range reporting
- [x] Public-domain Mill benchmark with two accepted reconstructions

## Post-v0.5 research directions

- expand reviewed public-domain / permission-compatible real-text corpora;
- add page/character anchor coordinates for scholarly editions and PDFs;
- add an adjudication UI for editing alignment units side-by-side;
- add calibrated semantic alignment proposals as an optional, separately auditable layer;
- optional hosted demo / GitHub Pages deployment.

## Evaluation

The evaluation layer is explicit about interpretive plurality. Stable-ID mode remains available, but unconstrained outputs can now be aligned through a separate JSON artifact before structural scoring. Multi-reference mode reports compatibility with several accepted reconstructions without collapsing them into a single synthetic gold graph. See `benchmark/README.md`, `docs/alignment.md`, and `docs/evaluation.md`.

## Non-goals

Discourse Atlas is not intended to replace close reading, claim one uniquely correct structure for interpretive texts, flatten every relation into premise/conclusion pairs, or treat textual order as logical dependence by default.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Release history is recorded in [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
