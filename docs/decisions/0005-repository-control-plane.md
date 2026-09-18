# 0005 — Repository-Backed Collaboration Control Plane

**Status:** Accepted
**Date:** 2026-09-18
**Decision authority:** Explicit maintainer authorization for v1.1.1 hardening
**Supersedes:** None
**Superseded by:** None
**Affected versions:** Toolkit 1.1.1; no graph/alignment schema change

## Context

`PROJECT_MANIFEST.yaml` existed as a machine-readable map, but repository consistency still duplicated release/schema versions as Python constants and task onboarding had no machine-readable route policy. This left the collaboration layer partially descriptive rather than executable.

## Decision

Use `PROJECT_MANIFEST.yaml` as the source for expected versions and repository resource locations. Add `PROJECT_CONTEXT_INTERFACE.yaml` as the repository-backed retrieval/control policy:

- task routes resolve manifest references rather than duplicating file paths;
- retrieval is selective and current-task scoped;
- latest repository state is read before high-impact actions and writes;
- touched session excerpts become stale after repository writes;
- revision conflicts are explicit failure states;
- high-impact semantic/schema/benchmark-reference/governance decisions distinguish AI proposals from maintainer decisions.

## Consequences

- CI consistency checks must derive expected version/path state from the Manifest;
- new route references must resolve to existing Manifest-declared repository resources;
- onboarding can remain lightweight without importing the full HARC Working Memory architecture;
- `PROJECT_STATUS.md` carries the minimal operational resume state needed for handoff;
- branch protection remains a repository-setting enforcement layer separate from the in-repository control plane.

## Affected canonical sources

- `PROJECT_MANIFEST.yaml`
- `PROJECT_CONTEXT_INTERFACE.yaml`
- `START_HERE.md` / `START_HERE.zh-CN.md`
- `AGENTS.md` / `AGENTS.zh-CN.md`
- `GOVERNANCE.md`
- `scripts/check_repository_consistency.py`
