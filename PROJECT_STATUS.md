# Project Status

Last updated: 2026-09-18

## Current release

- Toolkit/repository release: **1.1.0**
- Remote Agent protocol: **1.1.0**
- Current graph schema: **0.2.0**
- Supported legacy graph profile: **0.1.0**
- Alignment schema: **0.1.0**
- Hosted Atlas: <https://chongliuphil.github.io/discourse-atlas/>

## Current stage

**v1.1 — Collaboration, Governance & Reproducibility**

The v1.0 product surface is stable enough that the current priority is repository continuity: make canonical authority, version domains, compatibility, decisions, release procedure, and zero-context handoff explicit before another major analysis feature.

## v1.1 implemented

- separated product-facing `AGENT.md` from repository-facing `AGENTS.md`;
- added zero-context repository onboarding;
- added project manifest, current status, roadmap, governance, citation metadata, release docs, and Decision Records;
- established independent release/protocol/schema version domains;
- froze graph `0.1.0` legacy compatibility and moved current graph output to immutable `0.2.0`;
- added CLI dispatch for graph schema `0.1.0` and `0.2.0`;
- migrated maintained graph fixtures to `0.2.0`;
- expanded contribution, PR, security, and architecture documentation;
- committed the web npm lockfile and switched CI/Pages to `npm ci`;
- added automated repository-consistency checks.

## Operational state

### Current objective

Keep the v1.1.x collaboration control plane internally consistent and use it as the repository handoff baseline before starting another major research feature.

### Immediate next action

After the v1.1.1 hardening release is verified, select exactly one v1.2 candidate from `ROADMAP.md` before implementation begins.

### Active work

- v1.1.1 control-plane hardening: manifest-driven consistency, route-based selective retrieval, operational resume state, decision-authority labeling, and bilingual structural parity.

### Blockers

- None for v1.1.1.

### Pending maintainer decisions

- Which v1.2 candidate should be first.
- Whether to enable GitHub `main` branch protection / required status checks when repository-admin settings are available; CI gates currently exist but are not enforced by branch protection.

### Synchronization defects

- None known at the start of v1.1.1; CI is the verification authority for repository consistency.

## Known non-blocking debt

- `AGENT.md` and the modular Skill still intentionally duplicate methodology text; generating the remote protocol from canonical components is a later refactor.
- Release tags/GitHub Releases are not yet automated.

## Next

See `ROADMAP.md` for candidate research and engineering work after the v1.1 governance baseline.
