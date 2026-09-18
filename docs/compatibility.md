# Compatibility

## Current matrix

| Artifact | Current | Supported legacy | Notes |
|---|---:|---:|---|
| Toolkit / repository | 1.1.0 | — | Python + web + docs release line |
| Remote Agent protocol | 1.1.0 | Git history | New analyses follow current protocol |
| Discourse graph schema | 0.2.0 | 0.1.0 | CLI validates current and terminal legacy profile |
| Node alignment schema | 0.1.0 | — | Independent version domain |

## Graph compatibility

Graph `0.2.0` is the version for new maintained examples and new Agent output. It includes the fields present by v1.0, including optional `main_claim`, page ranges, and Unicode character ranges.

The CLI accepts `schema_version: 0.1.0` using `schemas/discourse-graph/0.1.0-legacy.schema.json`. This is a compatibility profile, not a claim that every historical 0.1.0 commit had the same schema. For exact historical reproducibility, pin the Git commit used.

## Promises

- relation direction will not be silently reinterpreted;
- schema version numbers will not be reused for materially different accepted document sets;
- removing legacy support requires release notes and migration guidance;
- viewer layout/collapse state is not canonical graph data unless a future schema explicitly adopts it;
- alignment versions are independent of graph schema versions.

## Research pinning

For reproducible scholarly work, record the Discourse Atlas release/commit SHA, graph schema version, source edition/file identity, any PDF ingestion manifest/hash, and alignment version/file when comparative evaluation is used.
