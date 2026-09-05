# Discourse Atlas

[![CI](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml)

**Discourse Atlas** is an open-source, agent-skill-first toolkit for reconstructing the hierarchical structure and logical dependencies of argumentative and expository texts.

It is designed for essays, philosophy, academic papers, theoretical books, legal reasoning, policy reports, and other texts where understanding **how the parts depend on one another** matters as much as understanding what each part says.

> Status: **v0.8.0 research preview.** The toolkit now includes deterministic PDF text-layer ingestion, scholarly page and Unicode code-point anchors, explicit split/merge alignment, multi-reference evaluation, an in-browser alignment adjudication workbench, a public-domain philosophy benchmark, the analysis skill, validator/exporters, and synchronized reader.

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
- **Explicit source preparation.** PDF extraction, OCR, cleanup, and interpretation must not be silently conflated.
- **Reconstruction, not revelation.** The output is a criticizable interpretation, not a claim to the single true structure of a text.

## Repository layout

```text
discourse-atlas/
├── skills/discourse-structure/   # Portable Agent Skill
├── schemas/                      # Graph + unit-alignment schemas
├── src/discourse_atlas/          # Validation, PDF ingestion, alignment, evaluation CLI
├── apps/web/                     # Interactive reader + alignment workbench
├── examples/mini-essay/          # Small end-to-end example
├── benchmark/                    # Synthetic + public-domain evaluation cases
├── tests/                        # Schema, ingestion, anchor, alignment, evaluation tests
├── docs/                         # Architecture, ingestion, anchors, alignment, evaluation
└── .github/workflows/            # CI
```

## Use as an Agent Skill

Copy `skills/discourse-structure/` into a client that supports the Agent Skills `SKILL.md` format. Ask the agent to analyze a text's discourse structure and produce `analysis.json` and `analysis.md`. The skill is intentionally model- and vendor-neutral.

Source anchors can use paragraph, line, page, and exact Unicode code-point character coordinates. PDF sources can first be converted to a reproducible page-delimited text representation with the optional PDF ingestion command. See `skills/discourse-structure/references/source-anchors.md` and `skills/discourse-structure/references/pdf-ingestion.md`.

## Installation and CLI

Core installation does not require a PDF library:

```bash
python -m pip install .
```

Install the optional PDF extra when text-layer ingestion is needed:

```bash
python -m pip install '.[pdf]'
```

Development installation includes PDF support and tests:

```bash
python -m pip install -e '.[dev]'
```

Core commands:

```bash
discourse-atlas validate examples/mini-essay/analysis.json
discourse-atlas mermaid examples/mini-essay/analysis.json
discourse-atlas dot examples/mini-essay/analysis.json

# Extract a PDF text layer into page-aware Unicode text + manifest
discourse-atlas ingest-pdf book.pdf

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

## PDF text ingestion

`discourse-atlas ingest-pdf book.pdf` writes two files by default:

- `book.txt`: normalized Unicode text with `\n\f\n` between PDF pages;
- `book.pages.json`: a page manifest containing the source PDF SHA-256, page count, empty-page count, Unicode code-point offsets, and exact character span for every page.

Existing outputs are protected unless `--force` is supplied. Password-protected PDFs that cannot be opened without a password are rejected.

The command reads the PDF **text layer only**. It does not perform OCR, layout repair, dehyphenation, or semantic cleanup. Image-only/scanned pages normally become empty page spans and trigger a warning. This is deliberate: source extraction remains auditable rather than being silently transformed. See `docs/pdf-ingestion.md`.

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

It supports collapse/expand, source ↔ graph evidence tracing, paragraph/line/page/character anchors, node/edge inspection, human correction, local file loading, and corrected-JSON export. Character anchors scroll ordinary text/Markdown sources by Unicode code-point span. Page-only navigation works with the form-feed page boundaries emitted by `ingest-pdf`.

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

### v0.8 — deterministic PDF text ingestion
- [x] Optional `pdf` package extra rather than a mandatory PDF dependency
- [x] Text-layer extraction with fixed form-feed page boundaries
- [x] SHA-256 + per-page Unicode character-span manifest
- [x] Empty-page reporting without hidden OCR
- [x] Controlled malformed/encrypted PDF failures and overwrite protection
- [x] CLI, unit tests, cross-Python CI, and installed-package smoke coverage

## Post-v0.8 research directions

The v0.8 research-preview core is feature-complete for the current project scope. Further work is research/extension rather than unfinished baseline functionality:

- expand reviewed public-domain / permission-compatible real-text corpora;
- add OCR only as an explicit provenance-preserving adapter, not a hidden fallback;
- add calibrated semantic alignment proposals as an optional, separately auditable layer;
- optional hosted demo / GitHub Pages deployment.

## Evaluation

The evaluation layer is explicit about interpretive plurality. Stable-ID mode remains available, but unconstrained outputs can be aligned through a separate JSON artifact before structural scoring. Multi-reference mode reports compatibility with several accepted reconstructions without collapsing them into a single synthetic gold graph. Source-coordinate overlap can use paragraph/line anchors or, when those are absent, character/page anchors. See `benchmark/README.md`, `docs/alignment.md`, `docs/alignment-workbench.md`, `docs/scholarly-anchors.md`, and `docs/evaluation.md`.

## Non-goals

Discourse Atlas is not intended to replace close reading, claim one uniquely correct structure for interpretive texts, flatten every relation into premise/conclusion pairs, treat textual order as logical dependence by default, or silently treat text extraction/OCR as interpretation-neutral operations.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Release history is recorded in [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
