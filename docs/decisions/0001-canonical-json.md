# 0001 — Canonical JSON Representation

**Status:** Accepted

## Context

Discourse Atlas has multiple renderers and interfaces. A visualization-specific model would couple research data to one UI.

## Decision

Portable JSON governed by JSON Schema is canonical. Mermaid, DOT, React Flow state, layout coordinates, and other views are derived representations.

## Consequences

Tools share one analysis artifact; UI state stays non-canonical unless explicitly adopted by schema; schema compatibility is a research-data concern.

## Canonical references

- `schemas/discourse-graph.schema.json`
- `docs/architecture.md`
