# Discourse Atlas

[English](README.md) | [中文](README.zh-CN.md)


[![CI](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml)
[![Pages](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/pages.yml/badge.svg)](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/pages.yml)

**Discourse Atlas** is an open-source protocol and toolkit for reconstructing the hierarchical argumentative structure of complex texts — from whole-work architecture down to local arguments.

It is designed for philosophy, essays, academic papers, theoretical books, legal reasoning, policy reports, and other texts where understanding **which parts support, require, refine, challenge, or respond to which other parts** matters as much as understanding what each part says.

> Status: **v1.1.0 collaboration-and-governance research release.** The v1.0 hosted product surface remains intact; v1.1 adds repository-backed onboarding, explicit canonical authority, immutable schema versioning, compatibility policy, Decision Records, release governance, and automated repository-consistency checks.

Hosted Interactive Atlas:

<https://chongliuphil.github.io/discourse-atlas/>

## Zero-install: give this URL to an AI agent

If your AI agent can read public URLs and can access the source document, **you do not need to install Discourse Atlas**.

Give the agent this protocol:

```text
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/AGENT.md
```

Then use a prompt such as:

```text
Read and follow the Discourse Atlas protocol:
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/AGENT.md

Analyze this source:
<SOURCE URL OR ATTACHED DOCUMENT>

Start with a readable work-level argument map. Identify the main claim and argumentative role of each major part/chapter, then recursively expand to section and local-argument level only where useful. Preserve authorial headings, mark inferred structure, ground major relations in evidence, and return canonical Discourse Atlas JSON when possible.
```

The remote protocol is intentionally self-contained. It tells the agent how to recover hierarchy, distinguish claims from summaries, infer relation directions, preserve uncertainty, attach evidence, and present a macro-to-micro map.

A remote URL is **not** the same as an installed Agent Skill. The standards-compatible Skill remains in `skills/discourse-structure/`; `AGENT.md` is a portable instruction entry point for browsing agents. See `docs/zero-install-agent.md`.

## What the resulting map represents

Discourse Atlas separates two structures:

1. **Containment hierarchy** — work → part → chapter → section → subsection → paragraph / argument unit.
2. **Discourse dependency graph** — relations such as `requires`, `supports`, `derives`, `refines`, `contrasts`, `objects_to`, and `responds_to`.

A node can distinguish:

- `title` — what the textual unit is called;
- `main_claim` — the proposition it advances, when it advances one;
- `summary` — what it discusses or does;
- `function` — its discourse function(s);
- `role_in_parent` — why it is needed inside the next higher level.

`main_claim` is intentionally optional: definitions, problem statements, examples, or surveys should not be forced into artificial theses.

The default visualization strategy is progressive disclosure:

```text
Work Map -> Part / Chapter Map -> Section Map -> Local Argument Map
```

A long book should therefore begin with a readable map of its central problem, central thesis, major chapters, chapter-level claims, and the most important relations between them — not hundreds of sentence-level nodes.

## Design principles

- **Structure before summary.** Recover architecture before writing global conclusions.
- **Macro before micro.** Make the whole composition intelligible before expanding local arguments.
- **Preserve authorial structure.** Existing chapters/sections outrank inferred segmentation.
- **Mark inferred structure explicitly.** AI-generated sections must never masquerade as authorial headings.
- **Separate hierarchy from dependency.** Containment is not logical support.
- **Separate claim from summary and role.** These answer different analytical questions.
- **Evidence important edges.** Major inferred relations should point back to the source.
- **Alignment before comparison.** Different segmentations must be aligned before structural differences are scored.
- **Explicit source preparation.** PDF extraction, OCR, cleanup, and interpretation must not be silently conflated.
- **Reconstruction, not revelation.** The output is a criticizable interpretation, not a claim to the single true structure.

## Repository layout

```text
discourse-atlas/
├── START_HERE.md / .zh-CN.md      # Zero-context repository onboarding
├── AGENT.md                       # Zero-install product-facing analysis protocol
├── AGENTS.md / AGENTS.zh-CN.md    # Repository collaboration contract
├── PROJECT_MANIFEST.yaml          # Machine-readable project/version map
├── PROJECT_STATUS.md              # Current development state
├── ROADMAP.md                     # Completed and candidate milestones
├── skills/discourse-structure/    # Portable standards-compatible Agent Skill
├── schemas/                       # Graph + unit-alignment schemas
├── src/discourse_atlas/           # Validation, PDF ingestion, alignment, evaluation CLI
├── apps/web/                      # Interactive reader + alignment workbench
├── examples/mini-essay/           # Small end-to-end example
├── benchmark/                     # Synthetic + public-domain evaluation cases
├── tests/                         # Schema, ingestion, anchor, alignment, evaluation tests
├── docs/                          # Protocol, architecture, ingestion, evaluation, hosted-atlas docs
└── .github/workflows/             # CI + GitHub Pages deployment
```

## Formal Agent Skill

For clients that support the Agent Skills `SKILL.md` format, load or copy `skills/discourse-structure/` into the client's skill directory. The Skill is model- and vendor-neutral and follows the same methodology as `AGENT.md`, with additional references loaded as needed.

The Skill now analyzes each useful unit in terms of `main_claim`, `summary`, `function`, `role_in_parent`, source evidence, and confidence, and explicitly builds the work-level map before drilling down.

## Canonical representation

The canonical representation is JSON. Visualizations are derived views, not the source of truth.

Canonical schema:

```text
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/schemas/discourse-graph.schema.json
```

New analyses use graph schema **`0.2.0`**. The CLI also supports the terminal legacy **`0.1.0` compatibility profile** for existing analyses. Versioned schemas are immutable; see `docs/versioning.md` and `docs/compatibility.md`.

## Interactive reader

Use the hosted Interactive Atlas without installing anything:

<https://chongliuphil.github.io/discourse-atlas/>

The web app in `apps/web/` turns the canonical graph into a synchronized reading environment with nested React Flow nodes and ELK layout.

It supports:

- nested/collapsible work → chapter → section structure;
- cross-hierarchy logical arrows;
- claim-first node cards with legacy summary fallback;
- authorial vs AI-inferred provenance;
- source ↔ graph evidence tracing;
- paragraph/line/page/Unicode-character anchors;
- node/edge inspection and human correction;
- corrected JSON export;
- an Alignment workspace for reviewing one-to-one and split/merge correspondences.

```bash
cd apps/web
npm install
npm run dev
```

Production deployment and release verification are documented in `docs/hosted-atlas.md`.

## Optional installation and CLI

Installation is **not required** for the zero-install agent workflow. Install the Python package when you want local validation, export, evaluation, alignment, or deterministic PDF text-layer ingestion.

Core installation:

```bash
python -m pip install .
```

Optional PDF extra:

```bash
python -m pip install '.[pdf]'
```

Development installation:

```bash
python -m pip install -e '.[dev]'
```

Commands:

```bash
discourse-atlas validate examples/mini-essay/analysis.json
discourse-atlas mermaid examples/mini-essay/analysis.json
discourse-atlas dot examples/mini-essay/analysis.json

discourse-atlas ingest-pdf book.pdf

discourse-atlas align reference.json candidate.json -o alignment.json
discourse-atlas evaluate reference.json candidate.json --alignment alignment.json
discourse-atlas multi-evaluate candidate.json ref-a.json ref-b.json --auto-align
discourse-atlas agreement ref-a.json ref-b.json --alignment alignment.json
```

## Relation ontology

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

See `skills/discourse-structure/references/relation-ontology.md`.

## PDF text ingestion and scholarly anchors

`discourse-atlas ingest-pdf book.pdf` produces:

- `book.txt` — normalized Unicode text with `\n\f\n` page separators;
- `book.pages.json` — PDF SHA-256, page count, empty-page count, and exact Unicode code-point span for every page.

The command reads the PDF text layer only. It does not silently run OCR, repair layout, dehyphenate, or semantically clean the source.

Source anchors can use:

- paragraph ranges: 1-based inclusive;
- line ranges: 1-based inclusive;
- page ranges: 1-based inclusive;
- `char_start`: 0-based inclusive Unicode code-point offset;
- `char_end`: 0-based exclusive Unicode code-point offset.

See `docs/pdf-ingestion.md` and `docs/scholarly-anchors.md`.

## Evaluation and interpretive plurality

Discourse Atlas does not assume that interpretive texts always have one uniquely correct segmentation. The evaluation layer supports explicit one-to-one, split, merge, and many-to-many unit alignments before structural scoring, and multi-reference evaluation can retain several defensible reconstructions.

The benchmark includes synthetic cross-genre cases and a public-domain John Stuart Mill *On Liberty* example with two accepted reconstructions and a reviewed split/merge alignment.

See `benchmark/README.md`, `docs/alignment.md`, `docs/alignment-workbench.md`, and `docs/evaluation.md`.

## Completed milestones

- **v0.1** — specification-first Skill, schema, ontology, validator, Mermaid/DOT exporters.
- **v0.2** — React Flow + ELK nested interactive map.
- **v0.3** — synchronized source reading and human correction.
- **v0.4** — benchmark and structural/evidence evaluation.
- **v0.5** — explicit alignment, multi-reference evaluation, public-domain Mill case.
- **v0.6** — browser alignment adjudication workbench.
- **v0.7** — scholarly page and Unicode character anchors.
- **v0.8** — deterministic PDF text-layer ingestion and provenance manifest.
- **v0.9** — zero-install remote agent protocol, claim-aware schema/Skill, and claim-first macro-to-micro viewer.
- **v1.0** — Hosted Interactive Atlas on GitHub Pages with repository-subpath-safe production assets and automated deployment.
- **v1.1** — repository collaboration contract, zero-context onboarding, immutable graph schema `0.2.0`, compatibility/version governance, Decision Records, citation metadata, and repository consistency checks.

## Post-v1.1 research directions

The v1.1 project combines the v1.0 research core with explicit collaboration and compatibility governance. Further work is extension/research rather than required setup:

- more reviewed public-domain or permission-compatible long-form philosophy corpora;
- OCR only as an explicit provenance-preserving adapter;
- calibrated semantic alignment proposals as an optional, separately auditable layer;
- deep-linkable agent-to-viewer handoff formats for opening generated maps directly in the hosted atlas.

## Non-goals

Discourse Atlas is not intended to replace close reading, claim one uniquely correct structure for interpretive texts, flatten every relation into premise/conclusion pairs, treat textual order as logical dependence by default, or silently treat extraction/OCR as interpretation-neutral.

## Contributing

Repository maintainers and AI agents should start with [START_HERE.md](START_HERE.md) and [AGENTS.md](AGENTS.md). See [CONTRIBUTING.md](CONTRIBUTING.md), [GOVERNANCE.md](GOVERNANCE.md), and [ROADMAP.md](ROADMAP.md). Release history is recorded in [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
