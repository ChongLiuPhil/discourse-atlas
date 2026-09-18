# Governance

Discourse Atlas is open research software. This document describes how durable project decisions are represented and reviewed.

## Roles

- **Maintainers** manage releases, merge pull requests, resolve compatibility questions, and steward canonical semantics.
- **Contributors** may propose code, documentation, benchmark, schema, ontology, or research changes through focused pull requests.
- **AI agents** may assist, but repository state and reviewed changes—not agent memory—constitute project decisions.

The repository owner/maintainers retain final merge and release authority.

## Decision classes

Routine implementation changes can normally be decided in a focused PR when they do not alter canonical semantics or compatibility.

Changes to relation meaning, segmentation, evidence interpretation, uncertainty semantics, or reconstruction contracts require explicit semantic documentation and synchronized protocol/Skill updates.

Changes to accepted JSON shape require a new schema version when the accepted document set changes.

Durable architectural choices should receive a short Decision Record under `docs/decisions/`.

## Review expectations

A reviewer should be able to determine the problem, governing canonical source, semantic/schema impact, compatibility impact, evidence/tests, and synchronized docs/fixtures.

## Releases

Release preparation follows `docs/release-process.md`. A release is not complete while version metadata, compatibility statements, examples, or deployment checks disagree.

## Research integrity

Benchmark/reference analyses remain criticizable research artifacts. Do not silently rewrite them merely to improve an implementation score. Preserve source provenance, uncertainty, and alternative defensible reconstructions where relevant.

## Security

Public examples/issues must not contain confidential manuscripts, credentials, or restricted source material. See `SECURITY.md`.
