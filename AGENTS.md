# AGENTS.md — Discourse Atlas Repository Collaboration Contract

[English](AGENTS.md) | [中文](AGENTS.zh-CN.md)

This file governs humans and AI agents maintaining the **Discourse Atlas repository**. It does not replace the user-facing `AGENT.md` reconstruction protocol.

## Repository-backed state

GitHub is the authoritative project state. Chat history, account memory, hidden scratchpads, local summaries, and earlier agent reports are non-authoritative. Before high-impact changes or writes, read the latest target files, `PROJECT_MANIFEST.yaml`, and `PROJECT_STATUS.md`.

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

AI agents may propose architecture and semantics, but proposals become durable project decisions only through repository changes and normal review. Long-lived architectural choices should receive a Decision Record when appropriate.

This lightweight governance layer borrows repository-backed continuity principles from HARC without importing HARC's full research-memory architecture.
