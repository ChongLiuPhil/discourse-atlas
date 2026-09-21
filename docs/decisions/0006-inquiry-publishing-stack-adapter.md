# 0006 — Adopt Inquiry Publishing Stack as a Product-Governance Adapter

**Status:** Accepted  
**Date:** 2026-09-21  
**Decision authority:** Explicit maintainer authorization for the account-wide Inquiry Publishing Stack audit and execution  
**Supersedes:** None  
**Superseded by:** None  
**Affected versions:** No toolkit/protocol/schema version change

## Context

Discourse Atlas already had a mature repository-backed control plane before account-wide Inquiry Publishing Stack adoption: `PROJECT_MANIFEST.yaml`, `PROJECT_CONTEXT_INTERFACE.yaml`, `PROJECT_STATUS.md`, Decision Records, versioned schemas, canonical semantic references, CI, release documentation, and a production GitHub Pages deployment.

Blindly installing the full research template would create duplicate authority for semantics, working state, releases, and publication.

## Decision

Adopt the current Inquiry Publishing Stack through a thin project-native adapter:

- AHICP is active, but maps onto the existing product-governance control plane rather than creating duplicate research Core / Working Memory structures.
- `PROJECT_MANIFEST.yaml` and `PROJECT_CONTEXT_INTERFACE.yaml` remain the routing and context-policy authorities.
- `PROJECT_STATUS.md` remains the operational resume state.
- Semantic/schema authority remains distributed across the versioned schemas, relation ontology, remote Agent protocol, Skill references, implementation, and Decision Records.
- PPF maps the already-authorized public GitHub Pages Hosted Atlas at `https://chongliuphil.github.io/discourse-atlas/`.
- `website.yaml publish=false` remains the Academic Vault / homepage-change boundary; it does not revoke the existing public Hosted Atlas.
- Toolkit/protocol/schema releases remain governed by `docs/release-process.md` and their independent version domains. A routine Pages deployment is public production delivery, not automatically a new toolkit release.

Stack v2 separates the Starter composition/template revisions frozen in `project-stack.lock.yaml` from the newer semantic AHICP/PPF/Vault revisions explicitly adopted by the project.

## Consequences

- No new Content Core, Form Core, research Framework Status, Argument Map, or full research Working Memory tree is introduced.
- No relation semantics, schema contract, Agent protocol, benchmark reference interpretation, toolkit version, provider, repository visibility, or existing public authorization changes.
- Existing CI and Pages deployment remain the implementation gates.
- Future Stack upgrades must preserve the distinction between template revisions, project semantic adoption revisions, public Hosted Atlas state, and Academic Vault homepage publication metadata.

## Affected canonical sources

- `AHICP_MANIFEST.yaml`
- `AHICP_CONTEXT_INTERFACE.yaml`
- `AHICP_ADOPTION.md`
- `project-stack.yaml`
- `project-stack.lock.yaml`
- `publishing.yaml`
- `PROJECT_MANIFEST.yaml`
- `PROJECT_CONTEXT_INTERFACE.yaml`
- `PROJECT_STATUS.md`
- `scripts/check_repository_consistency.py`
