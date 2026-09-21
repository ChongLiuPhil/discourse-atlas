# AGENTS.md — Discourse Atlas Repository Collaboration Contract

[English](AGENTS.md) | [中文](AGENTS.zh-CN.md)

This file governs humans and AI agents maintaining the **Discourse Atlas repository**. It does not replace the user-facing `AGENT.md` reconstruction protocol.

## Repository-backed state

GitHub is the authoritative project state. Chat history, account memory, hidden scratchpads, local summaries, and earlier agent reports are non-authoritative. `PROJECT_MANIFEST.yaml` locates canonical resources; `PROJECT_CONTEXT_INTERFACE.yaml` controls selective retrieval. Before high-impact changes or writes, read the latest target files and the route-required repository state.

## Context routing and cache

Classify work as **SEMANTICS**, **SCHEMA**, **IMPLEMENTATION**, **WEB**, **BENCHMARK**, **DOCS**, **RELEASE**, or **GOVERNANCE**, then resolve the route in `PROJECT_CONTEXT_INTERFACE.yaml`.

Retrieve only the minimum canonical state needed for the task. Session excerpts are non-authoritative cache. Read latest before high-impact actions and writes; after a write, treat touched excerpts as stale and refetch affected dependencies when later reasoning still relies on them. Prefer Git commit/blob SHAs or equivalent revision tokens when coordinating concurrent work.

## Product protocol vs repository contract

- `AGENT.md`: self-contained remote protocol for **using** Discourse Atlas.
- `skills/discourse-structure/SKILL.md`: modular installed Skill implementing the reconstruction methodology.
- `AGENTS.md`: contract for **maintaining** the repository.

## Canonical authority

| Concern | Canonical authority |
|---|---|
| graph JSON shape | versioned graph schema |
| alignment JSON shape | versioned alignment schema |
| relation meaning/direction | `skills/discourse-structure/references/relation-ontology.md` |
| source-coordinate semantics | `skills/discourse-structure/references/source-anchors.md` |
| segmentation methodology | `skills/discourse-structure/references/segmentation-rules.md` |
| reconstruction workflow | `AGENT.md` + Skill, kept semantically aligned |
| implementation behavior | tests + source code |
| architecture rationale | `docs/architecture.md` + Decision Records |
| release/version policy | `docs/versioning.md` |
| current project state | `PROJECT_STATUS.md` |
| public introduction | README; explanatory, not normative |

README must not silently redefine schema or ontology semantics.

## Change propagation

Semantic changes should update the canonical reference, `AGENT.md`, Skill, tests/examples, and any affected schema/evaluation logic. Do not silently broaden relation semantics.

Schema changes must create a new immutable versioned schema when the accepted document set changes; update the latest alias, packaged resources, fixtures, compatibility tests, and migration/version documentation. Never reuse a schema version for a materially different contract.

Web/CLI behavior changes require tests and user documentation. Benchmark changes must preserve provenance and must not rewrite references merely to improve a metric.

## Version domains

Toolkit/release, remote Agent protocol, graph schema, and alignment schema are independent version domains. Follow `docs/versioning.md`.

## Bilingual governance

English is canonical for technical governance. The synchronized entry pairs are README, START_HERE, and AGENTS. Language-neutral code, schemas, data, and most technical docs remain single-copy.

## Pull requests

Keep PRs focused. State change class, rationale, canonical sources, schema/ontology impact, compatibility/version impact, security/privacy impact where relevant, and validation performed.

## AI proposals

AI agents may propose architecture and semantics, but a polished proposal is not a maintainer decision. For changes to relation semantics, reconstruction methodology, persisted schema contracts, benchmark reference interpretations, or governance authority, the PR must identify decision authority as an existing documented decision, explicit maintainer authorization, or `AI-PROPOSED / awaiting maintainer decision`. An unresolved AI proposal must not be merged as though it were approved.

Long-lived architectural choices should receive a Decision Record when appropriate.

This lightweight governance layer borrows repository-backed continuity principles from HARC without importing HARC's full research-memory architecture.


## Current Inquiry Publishing Stack adapter

AHICP is the current protocol entry, but it delegates repository routing and decision policy to the existing `PROJECT_MANIFEST.yaml` / `PROJECT_CONTEXT_INTERFACE.yaml` control plane. Do not create duplicate research Content Core, Form Core, Framework Status, Argument Map, or full Working Memory structures for template symmetry.

PPF records the existing public GitHub Pages lifecycle. The Hosted Atlas is already authorized and production-active. `website.yaml publish=false` is a separate Academic Vault/homepage-change boundary. Toolkit/protocol/schema releases remain governed by `docs/release-process.md` and their independent version domains.
