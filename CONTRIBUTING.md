# Contributing to Discourse Atlas

Discourse Atlas is specification-first research software. Start with `START_HERE.md`, `PROJECT_MANIFEST.yaml`, and `AGENTS.md`.

## Change classes

Mark one or more: semantics/protocol, schema, Python/CLI, web/viewer, benchmark/evaluation, documentation, release/infrastructure, governance.

## Development

Python development uses `python -m pip install -e '.[dev]'`, `pytest`, and `python scripts/check_repository_consistency.py`.

Web development uses `npm ci`, `npm test`, and `npm run build` in `apps/web`. Use `npm install` only when intentionally updating dependency declarations/lock state.

## Semantic and ontology changes

For a new or changed relation, explain meaning, direction, difference from existing relations, a positive example, a tempting false positive, and compatibility impact. Update the canonical relation ontology first, then synchronize the remote protocol, Skill, tests/examples, and affected schema/evaluation logic.

## Schema changes

Follow `docs/versioning.md` and `docs/compatibility.md`. Update the immutable versioned schema, latest alias, packaged resource, validator dispatch, maintained fixtures, compatibility tests/docs, and manifest as applicable. Do not change the accepted document set while retaining the same version.

## Benchmark contributions

Use legally redistributable/public-domain sources, record provenance, keep reference interpretations reviewable, and do not modify gold/reference structure merely to improve a score.

## Bilingual entry documents

Substantive changes to README, START_HERE, or AGENTS should update their Chinese mirror in the same work cycle. Most technical documentation remains English-canonical.

## Pull requests

Keep PRs focused and complete the PR template. Explain compatibility/version impact, not only implementation details.
