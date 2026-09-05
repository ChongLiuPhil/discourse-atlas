# Changelog

All notable project changes are recorded here. Discourse Atlas is currently an alpha/research-preview project; the canonical graph schema remains at `0.1.0` while the toolkit release is `0.8.0`.

## 0.8.0 — 2026-09-05

### Added
- Optional `pdf` installation extra using `pypdf` 6.x while keeping the core installation PDF-library-free.
- `ingest-pdf` CLI command for deterministic PDF text-layer extraction.
- Fixed `\n\f\n` page separators compatible with the v0.7 page-aware web reader.
- Page manifest with PDF SHA-256, page count, empty-page count, Unicode code-point offset unit, total character count, and exact character span for every page.
- Output overwrite protection with explicit `--force` opt-in.
- Controlled errors for malformed PDFs, unsupported password-protected PDFs, and page-level extraction failures.
- Explicit empty-page warnings; OCR is not performed silently.
- PDF ingestion documentation and Agent Skill source-preparation guidance.
- Python regression tests for multilingual offsets, empty pages, provenance hashes, CLI output behavior, overwrite protection, and malformed PDFs.
- Installed-package CI smoke coverage for the PDF extra and `ingest-pdf` command.

### Changed
- The Skill now begins with an explicit source-preparation pass before structural reconstruction.
- Development installs include the optional PDF dependency so ingestion is tested across Python 3.10–3.13.
- Python and web package versions advance to `0.8.0`.

## 0.7.0 — 2026-09-05

### Added
- Optional `page_start` / `page_end` anchors for fixed editions and PDF-derived text.
- Optional exact `char_start` / `char_end` anchors using 0-based Unicode code-point offsets with an exclusive end.
- Semantic validation for page and character ranges, including missing-start and empty/reversed character spans.
- Page/character fallback support in deterministic alignment and alignment-aware evidence scoring.
- Unicode-aware browser source-block coordinates and character-anchor navigation.
- Form-feed (`\f`) page-boundary support for page-only evidence navigation in extracted text.
- Inspector labels for page, paragraph, line, and character coordinates.
- Skill and software documentation for scholarly source-anchor conventions.
- Python and Node regression coverage for page fallback, character overlap, multilingual code-point offsets, and coordinate priority.

### Changed
- Automatic anchor matching keeps paragraph/line coordinates first, then character spans, then page ranges, then section labels.
- Character overlap metrics use fixed 32-code-point cells for scalability while stored coordinates remain exact.
- Python and web package versions advance to `0.7.0`; the canonical graph schema version remains `0.1.0` because the new fields are optional and backward compatible.

## 0.6.0 — 2026-09-05

### Added
- Browser-based alignment adjudication workbench alongside the synchronized reader.
- Side-by-side node selection for reference and candidate reconstructions.
- Accept/propose/reject state editing with unmatched-node recovery after rejection.
- Manual one-to-one and split/merge reviewed-unit creation with rationale capture.
- Alignment coverage indicators, duplicate/unknown membership checks, and reviewed JSON export.
- Browser implementation of the deterministic anchor-overlap proposal algorithm plus Node regression tests.
- Bundled Mill multi-reference alignment example in the web build.

### Changed
- The web root now switches between Reader and Alignment workspaces without changing the existing reader state machine.
- Python and web package versions advance to `0.6.0`.

## 0.5.0 — 2026-09-05

### Added
- Explicit unit-alignment JSON format supporting one-to-one, split, merge, and many-to-many reviewed correspondences.
- `align` command for deterministic, inspectable source-anchor overlap proposals.
- Alignment-aware `evaluate` and `agreement` modes that compare evidence by source coordinates instead of anchor IDs.
- `multi-evaluate` for scoring a candidate against several defensible references while preserving per-reference results.
- Public-domain John Stuart Mill *On Liberty* benchmark excerpt with two accepted reconstructions and a reviewed split/merge alignment.
- Alignment schema, alignment methodology documentation, library tests, and installed-package CLI smoke coverage.

### Changed
- Evaluation now explicitly separates segmentation/alignment error from hierarchy/relation/evidence error.
- Benchmark manifest supports multiple reference graphs per case while retaining a backward-compatible primary `gold` entry.
- Python and web package versions advance to `0.5.0`.

## 0.4.0 — 2026-09-03

### Added
- Evaluation CLI commands: `evaluate` and `agreement`.
- Structural, relation, node-anchor, and edge-evidence metrics.
- Symmetric treatment of `contrasts` during evaluation.
- Benchmark protocol and four project-authored cross-genre synthetic cases.
- Ontology review decision record and evaluation philosophy documentation.

### Changed
- CI now verifies Python 3.10–3.13, normal wheel installation, evaluation commands outside the repository checkout, and the production web build.
- GitHub Actions use current `checkout`, `setup-python`, and `setup-node` major versions.

### Fixed
- Corrected relation directions in benchmark annotations to match the ontology.
- Ensured the installed CLI exposes evaluation commands, not only editable-development installs.

## 0.3.0 — 2026-09-03

### Added
- Synchronized three-pane reader: source text, discourse graph, and reconstruction inspector.
- Paragraph and line evidence anchors.
- Source-to-graph highlighting and graph-to-source navigation.
- Human correction workflow with corrected JSON export.
- Local analysis/source file loading.

## 0.2.0 — 2026-09-03

### Added
- React Flow nested/compound graph viewer.
- ELK layered layout with cross-hierarchy dependency edges.
- Collapsible hierarchy with edge projection to visible ancestors.
- Visual provenance for authorial vs AI-inferred structure.

## 0.1.0 — 2026-09-03

### Added
- Portable `discourse-structure` Agent Skill.
- Canonical JSON Schema and nine-relation MVP ontology.
- Segmentation and analysis principles.
- Semantic graph validator and Mermaid/Graphviz exporters.
- Mini-essay end-to-end example.
- MIT license, contribution/security/conduct documents, issue/PR templates, tests, and CI.
