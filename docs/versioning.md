# Versioning Policy

Discourse Atlas uses separate version domains because software releases, analysis protocols, and persisted data contracts change at different rates.

## Current versions

- Toolkit / repository release: **1.1.0**
- Remote Agent protocol: **1.1.0**
- Discourse graph schema: **0.2.0**
- Node alignment schema: **0.1.0**

New graph outputs should declare `schema_version: "0.2.0"`.

The immutable current graph schema is `schemas/discourse-graph/0.2.0.schema.json`. The root `schemas/discourse-graph.schema.json` is only the latest alias.

## Schema version rules

Use semantic-version intent for persisted contracts:

- **MAJOR** — incompatible structural change requiring migration or rejecting previously valid documents;
- **MINOR** — accepted document set changes through backward-compatible additions or new optional capabilities;
- **PATCH** — clarification/fix that does not materially change the accepted document set.

Once a versioned schema path is published, do not silently replace it with a materially different contract.

## Historical graph 0.1.0 note

From project v0.1 through v1.0, the root graph schema retained `schema_version: 0.1.0` while optional page/character anchors and `main_claim` were added. Because unknown properties are rejected, the accepted document set changed even though the version string did not. That was a versioning defect.

v1.1 stops that drift by freezing a terminal legacy compatibility profile at `schemas/discourse-graph/0.1.0-legacy.schema.json`, moving maintained/current output to `0.2.0`, and making the CLI dispatch validation by declared version.

The legacy profile accepts additive 0.1-era fields used across v0.1–v1.0. Exact earlier historical schema snapshots remain reproducible by Git commit.

## Release synchronization

Toolkit releases synchronize `pyproject.toml`, `src/discourse_atlas/__init__.py`, `apps/web/package.json`, `PROJECT_MANIFEST.yaml`, `PROJECT_STATUS.md`, `CITATION.cff`, `CHANGELOG.md`, and README status text.

Protocol and schema versions change only when their own contracts change.

See `docs/compatibility.md` and `docs/release-process.md`.
