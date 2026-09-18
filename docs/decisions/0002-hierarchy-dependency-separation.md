# 0002 — Separate Hierarchy from Discourse Dependency

**Status:** Accepted

## Context

Textual containment and argumentative/discourse dependence answer different questions.

## Decision

Represent containment with `parent_id` and discourse/logical dependence with explicit edges.

## Consequences

Nested visualization does not imply logical support; cross-hierarchy edges are permitted; containment remains one rooted acyclic hierarchy while dependency need not be acyclic.

## Canonical references

- `schemas/discourse-graph.schema.json`
- `skills/discourse-structure/references/relation-ontology.md`
- `docs/architecture.md`
