# START HERE — Discourse Atlas Repository Onboarding

[English](START_HERE.md) | [中文](START_HERE.zh-CN.md)

This is the zero-context entry point for maintainers and AI agents working **on the Discourse Atlas repository**.

> `AGENT.md` is the product-facing protocol for using Discourse Atlas to analyze texts.  
> `AGENTS.md` is the repository collaboration contract for maintaining Discourse Atlas.  
> Do not confuse these roles.

## Required read order

Before substantive repository changes, read:

1. `PROJECT_MANIFEST.yaml`
2. `PROJECT_CONTEXT_INTERFACE.yaml`
3. `PROJECT_STATUS.md`
4. `AGENTS.md`
5. `ROADMAP.md`
6. classify the task route and selectively read its `required_refs`
7. the canonical files relevant to the requested change
8. `docs/versioning.md` and `docs/compatibility.md` for schema/protocol/release work
9. relevant Decision Records under `docs/decisions/`

The repository is authoritative project state. Chat history, model memory, and earlier summaries are transient context.

## Classify the change

Use one or more routes: **SEMANTICS**, **SCHEMA**, **IMPLEMENTATION**, **WEB**, **BENCHMARK**, **DOCS**, **RELEASE**, or **GOVERNANCE**.

`PROJECT_CONTEXT_INTERFACE.yaml` defines the required/optional repository references for each route. Retrieve only what the task needs; do not copy the whole repository into session context.

Before writing, refetch the latest target files. After a repository write, earlier excerpts of touched files are stale. For semantic or schema changes, also read the governing ontology/schema and relevant Decision Records.

## Completion criterion

A change is complete only when affected canonical sources, dependent implementation/docs/examples, compatibility/version statements, and tests are synchronized.

English is the technical canonical language for repository governance. Chinese README, START_HERE, and AGENTS files are synchronized onboarding mirrors.


## Current Inquiry Publishing Stack adapter

AHICP is a thin adapter over the repository-native product control plane. `PROJECT_MANIFEST.yaml`, `PROJECT_CONTEXT_INTERFACE.yaml`, `PROJECT_STATUS.md`, schemas, semantic references, release docs, and Decision Records remain authoritative. PPF maps the already-public GitHub Pages Hosted Atlas. `website.yaml publish=false` only blocks a new or changed Academic Vault/homepage publication; it does not revoke the existing Hosted Atlas.
