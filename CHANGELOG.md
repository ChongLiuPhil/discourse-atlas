# Changelog

All notable project changes are recorded here. Discourse Atlas remains research software; the toolkit release is `1.1.1`, the current graph schema is `0.2.0`, and graph `0.1.0` remains supported through a frozen legacy compatibility profile.

## Unreleased

### Governance
- Adopt current Inquiry Publishing Stack through a thin AHICP adapter over the existing product control plane.
- Add a PPF lifecycle contract for the already-public GitHub Pages Hosted Atlas without changing provider, public authorization, toolkit release version, Agent protocol version, or schema versions.
- Record Decision 0006 and validate Stack v2 template/adopted revision semantics through repository consistency CI.

## 1.1.1 — 2026-09-18

### Added
- `PROJECT_CONTEXT_INTERFACE.yaml` for repository-backed task routing, selective retrieval, revision/cache policy, trust boundary, and decision-policy states.
- Operational resume fields in `PROJECT_STATUS.md` and Decision Record 0005 for the collaboration control plane.
- Manifest-driven bilingual entry parity checks for heading structure and link targets.

### Changed
- Repository consistency now derives expected release/protocol/schema versions and resource locations from `PROJECT_MANIFEST.yaml` instead of duplicating those values in Python constants.
- PR/Issue change classes now use the same route names as the context interface.
- Governance and the PR template now distinguish routine implementation, documented/explicit maintainer decisions, and `AI-PROPOSED` changes awaiting a decision.
- Toolkit and web package versions advance to `1.1.1`; remote Agent protocol remains `1.1.0`, graph schema remains `0.2.0`, and alignment schema remains `0.1.0`.

## 1.1.0 — 2026-09-18

### Added
- Repository-facing `AGENTS.md` / `AGENTS.zh-CN.md` collaboration contract, distinct from product-facing `AGENT.md`.
- Bilingual zero-context `START_HERE` onboarding, project manifest/status/roadmap/governance, citation metadata, release documentation, and Decision Records.
- Immutable graph schema `0.2.0` plus a terminal legacy `0.1.0` compatibility profile.
- Automated repository consistency checks.
- Reproducible web dependency lockfile (`apps/web/package-lock.json`).

### Changed
- Toolkit and web package versions advance to `1.1.0`.
- Remote Agent protocol advances to `1.1.0` and requires new graph output to use schema `0.2.0`.
- Maintained examples, Skill example, benchmark annotations, and reference graphs migrate to graph schema `0.2.0`.
- CLI validation dispatches by declared graph schema version and supports both `0.1.0` and `0.2.0`.
- Contribution, PR, security, architecture, and hosted-atlas documentation now reflect the v1.x project surface and trust boundary.
- CI and Pages now install web dependencies with `npm ci` from the committed lockfile.

### Governance
- English is the technical canonical language; README, START_HERE, and AGENTS are synchronized bilingual entry pairs.
- README remains explanatory rather than a normative ontology/schema source.
- New schema version numbers must not be reused for materially different accepted document sets.

## 1.0.0 — 2026-09-16

### Added
- Hosted Interactive Atlas at `https://chongliuphil.github.io/discourse-atlas/`.
- GitHub Pages deployment workflow using the official Pages artifact/deployment actions.
- Hosted-atlas deployment and verification documentation.

### Changed
- Vite production base is now `/discourse-atlas/` for repository-scoped GitHub Pages assets.
- Root protocol and README now point readers from canonical JSON to the hosted browser atlas.
- Python and web package versions advance to `1.0.0`.

### Deployment
- GitHub Pages uses **Source = GitHub Actions** and deploys the static `apps/web/dist/` artifact to the `github-pages` environment.
- The Pages workflow runs the web tests and production build before deployment.

## 0.9.0 — 2026-09-16

### Added
- Root-level `AGENT.md` as a self-contained zero-install protocol that can be sent directly to any AI agent with public URL and source-reading access.
- Human-facing `docs/zero-install-agent.md` with a copy/paste prompt and source-access boundaries.
- Optional `main_claim` field on discourse nodes, preserving backward compatibility with earlier graphs.
- Macro-to-micro reconstruction guidance: work map → chapter map → section map → local argument map.
- Viewer rendering and Inspector editing for node main claims, with summary fallback for legacy graphs.
- Regression coverage for the remote protocol links and `main_claim` schema compatibility.

### Changed
- The formal Agent Skill now distinguishes `main_claim`, `summary`, `function`, and `role_in_parent` and builds the work-level map before expanding local arguments.
- The bundled mini-essay example now includes explicit main claims at work and section levels.
- Graph node layout allocates more space for claim-first reading at both container and leaf levels.
- Python and web package versions advance to `0.9.0`.

### Compatibility
- A URL is not presented as an installed Agent Skill. The formal `SKILL.md` directory remains standards-compatible; `AGENT.md` is a portable remote instruction entry point for browsing agents.
- The canonical graph schema version remains `0.1.0` because `main_claim` is optional and existing v0.1–v0.8 graph files remain valid.

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
