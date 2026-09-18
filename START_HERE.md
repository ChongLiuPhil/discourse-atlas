# START HERE — Discourse Atlas Repository Onboarding

[English](START_HERE.md) | [中文](START_HERE.zh-CN.md)

This is the zero-context entry point for maintainers and AI agents working **on the Discourse Atlas repository**.

> `AGENT.md` is the product-facing protocol for using Discourse Atlas to analyze texts.  
> `AGENTS.md` is the repository collaboration contract for maintaining Discourse Atlas.  
> Do not confuse these roles.

## Required read order

Before substantive repository changes, read:

1. `PROJECT_MANIFEST.yaml`
2. `PROJECT_STATUS.md`
3. `AGENTS.md`
4. `ROADMAP.md`
5. the canonical files relevant to the requested change
6. `docs/versioning.md` and `docs/compatibility.md` for schema/protocol/release work
7. relevant Decision Records under `docs/decisions/`

The repository is authoritative project state. Chat history, model memory, and earlier summaries are transient context.

## Classify the change

Use one or more routes: **SEMANTICS**, **SCHEMA**, **IMPLEMENTATION**, **WEB**, **BENCHMARK**, **DOCS**, **RELEASE**, or **GOVERNANCE**.

Before writing, refetch the latest target files. For semantic or schema changes, also read the governing ontology/schema and relevant Decision Records.

## Completion criterion

A change is complete only when affected canonical sources, dependent implementation/docs/examples, compatibility/version statements, and tests are synchronized.

English is the technical canonical language for repository governance. Chinese README, START_HERE, and AGENTS files are synchronized onboarding mirrors.
