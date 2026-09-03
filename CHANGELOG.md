# Changelog

All notable project changes are recorded here. Discourse Atlas is currently an alpha/research-preview project; the canonical graph schema remains at `0.1.0` while the toolkit release is `0.4.0`.

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
