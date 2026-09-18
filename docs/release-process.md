# Release Process

## 1. Define scope

Keep semantic, schema, infrastructure, and research-corpus changes distinguishable. Add/update a Decision Record for durable architectural rules. Identify compatibility impact before changing versions.

## 2. Update version domains

Bump only domains that changed.

Toolkit releases synchronize `pyproject.toml`, `src/discourse_atlas/__init__.py`, `apps/web/package.json`, `PROJECT_MANIFEST.yaml`, `PROJECT_STATUS.md`, `CITATION.cff`, `CHANGELOG.md`, and README status text.

Agent protocol changes update the version in `AGENT.md`. Schema changes create a new immutable versioned file, update aliases/resources, migrate maintained fixtures, and test supported legacy versions.

## 3. Validate

Required gates are the Python test matrix, installed-package smoke test, maintained graph fixture validation, web tests/build, and repository consistency check. Production Pages releases also require successful main-branch deployment and hosted-endpoint verification.

## 4. Review documentation

Check README bilingual status, START_HERE/AGENTS parity when governance changes, versioning/compatibility docs, SECURITY when the trust boundary changes, CHANGELOG, and CITATION metadata.

## 5. Merge and verify

Use a focused PR; squash is preferred for a focused release unit. After merge, verify main CI and Pages deployment.

## 6. Reproducibility token

When tags/GitHub Releases are used, tag the exact main commit. Until release automation is introduced, the commit SHA remains the most precise reproducibility token.
