# Discourse Atlas

[![CI](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml)

**Discourse Atlas** is an open-source, agent-skill-first toolkit for reconstructing the hierarchical structure and logical dependencies of argumentative and expository texts.

It is designed for essays, philosophy, academic papers, theoretical books, legal reasoning, policy reports, and other texts where understanding **how the parts depend on one another** matters as much as understanding what each part says.

> Status: **v0.7.0 research preview.** The toolkit now supports scholarly page and Unicode code-point character anchors in addition to paragraph/line grounding, explicit split/merge alignment, multi-reference evaluation, an in-browser alignment adjudication workbench, a public-domain philosophy benchmark, the analysis skill, validator/exporters, and synchronized reader.

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
├── apps/web/                     # Interactive reader + alignment workbench
├── examples/mini-essay/          # Small end-to-end example
├── benchmark/                    # Synthetic + public-domain evaluation cases
├── tests/                        # Schema, anchor, alignment, evaluation tests
├── docs/                         # Architecture, ontology, anchors, alignment, evaluation
└── .github/workflows/            # CI
```

## Use as an Agent Skill

Copy `skills/discourse-structure/` into a client that supports the Agent Skills `SKILL.md` format. Ask the agent to analyze a text's discourse structure and produce `analysis.json` and `analysis.md`. The skill is intentionally model- and vendor-neutral.

Source anchors can use paragraph, line, page, and exact Unicode code-point character coordinates. See `skills/discourse-structure/references/source-anchors.md`.

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

Validation checks JSON shape plus unique IDs, parent references, containment cycles, edge endpoints, evidence anchors, and paragraph/line/page/character coordinate ranges. Alignment validation checks unknown nodes, duplicate membership, and ambiguous repeated mappings.

## Scholarly source anchors

The canonical graph supports:

- paragraph ranges: 1-based, inclusive;
- line ranges: 1-based, inclusive;
- page ranges: 1-based, inclusive;
- `char_start`: 0-based, inclusive Unicode code-point offset;
- `char_end`: 0-based, exclusive Unicode code-point offset.

Character offsets are Unicode code points rather than UTF-8 bytes or JavaScript UTF-16 code units, so Python and browser behavior remains consistent for multilingual text. Deterministic alignment keeps paragraph/line coordinates first, then character spans, then page ranges, then section labels. See `docs/scholarly-anchors.md`.

## Interactive reader

The web app in `apps/web/` turns the canonical graph into a synchronized reading environment with nested React Flow nodes and ELK layout.

```bash
cd apps/web
npm install
npm run dev
```

It supports collapse/expand, source ↔ graph evidence tracing, paragraph/line/page/character anchors, node/edge inspection, human correction, local file loading, and corrected-JSON export. Character anchors scroll ordinary text/Markdown sources by Unicode code-point span. Page-only navigation works when extracted text preserves page breaks as form-feed (`\f`) separators.

Switch the web workspace to **Alignment** to review proposals, accept/reject correspondences, build split/merge units, and export reviewed alignment JSON.

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

### v0.6 — alignment adjudication UI
- [x] Reader / Alignment workspace switcher
- [x] Side-by-side reconstruction node selection
- [x] Accept / reject / retain proposal states
- [x] Manual one-to-one and split/merge unit creation
- [x] Coverage, membership validation, rationale capture, and reviewed JSON export
- [x] Browser proposal logic covered by Node tests

### v0.7 — scholarly source anchors
- [x] Page coordinates for fixed editions and PDF-derived text
- [x] Exact Unicode code-point character spans
- [x] Semantic validation for new coordinate ranges
- [x] Page/character-aware alignment and evidence evaluation
- [x] Browser evidence tracing and coordinate labels
- [x] Python/Node regression tests for multilingual character offsets and page fallbacks

## Post-v0.7 research directions

- expand reviewed public-domain / permission-compatible real-text corpora;
- add an explicit PDF text-ingestion layer that emits page-aware source text without making OCR a hidden dependency;
- add calibrated semantic alignment proposals as an optional, separately auditable layer;
- optional hosted demo / GitHub Pages deployment.

## Evaluation

The evaluation layer is explicit about interpretive plurality. Stable-ID mode remains available, but unconstrained outputs can be aligned through a separate JSON artifact before structural scoring. Multi-reference mode reports compatibility with several accepted reconstructions without collapsing them into a single synthetic gold graph. Source-coordinate overlap can use paragraph/line anchors or, when those are absent, character/page anchors. See `benchmark/README.md`, `docs/alignment.md`, `docs/alignment-workbench.md`, `docs/scholarly-anchors.md`, and `docs/evaluation.md`.

## Non-goals

Discourse Atlas is not intended to replace close reading, claim one uniquely correct structure for interpretive texts, flatten every relation into premise/conclusion pairs, treat textual order as logical dependence by default, or pretend that coordinate support itself is PDF extraction/OCR.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Release history is recorded in [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
