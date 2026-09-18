# 0004 — Immutable Schema Versioning

**Status:** Accepted in v1.1

## Context

Graph schema `0.1.0` was widened with optional fields between v0.1 and v1.0 while retaining the same version label.

## Decision

Starting with `0.2.0`, publish immutable versioned schema paths, keep root files only as latest aliases, dispatch CLI validation by declared version, preserve a terminal `0.1.0` compatibility profile, and never reuse a version number for a materially different accepted document set.

## Consequences

Maintained fixtures migrate to `0.2.0`; old `0.1.0` analyses remain accepted through the compatibility profile; exact old behavior remains pin-able by Git commit.

## Canonical references

- `docs/versioning.md`
- `docs/compatibility.md`
- `schemas/discourse-graph/`
