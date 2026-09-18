# Discourse Atlas Roadmap

## Completed

### v0.1–v0.9 — Research core

Schema-first discourse graphs, relation ontology, nested visualization, source synchronization, evaluation/alignment, scholarly anchors, deterministic PDF text-layer ingestion, and the zero-install remote Agent protocol.

### v1.0 — Hosted Interactive Atlas

GitHub Pages deployment with repository-subpath-safe production assets and automated deployment verification.

### v1.1 — Collaboration, Governance & Reproducibility

- [x] separate product `AGENT.md` from repository `AGENTS.md`;
- [x] add zero-context repository onboarding;
- [x] add project manifest, current status, roadmap, governance, citation metadata, and Decision Records;
- [x] define canonical authority and change propagation;
- [x] establish independent version domains and compatibility policy;
- [x] move current graph schema to immutable `0.2.0` while supporting legacy `0.1.0`;
- [x] expand contribution, PR, security, release, and architecture documentation;
- [x] add repository consistency checks;
- [x] commit the web npm lockfile and use `npm ci` in CI/Pages.

## Candidate v1.2 work

- generate self-contained `AGENT.md` from smaller canonical protocol components and verify zero drift;
- define a deep-linkable Agent → Hosted Atlas handoff format;
- add more reviewed public-domain or permission-compatible long-form philosophy corpora;
- add optional provenance-preserving OCR adapters;
- explore calibrated semantic alignment proposals as a separately auditable layer;
- expand schema migration tooling if future versions require transformations.

## Research agenda

- measure reconstruction agreement across expert and model annotators;
- study uncertainty calibration for inferred discourse relations;
- compare macro-to-micro maps with flat summaries for long-form comprehension;
- study how alternative defensible segmentations affect evaluation;
- test cross-model portability of the zero-install protocol and Skill;
- study whether repository-backed governance reduces semantic/version drift across long development cycles.
