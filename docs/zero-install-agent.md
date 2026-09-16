# Zero-install agent workflow

Discourse Atlas can be used without installing the Python package or copying the Agent Skill directory.

The zero-install path is intended for any AI agent that can read a public URL and access the source document.

## One URL to give the agent

Use this stable raw entry point:

```text
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/AGENT.md
```

That file is deliberately self-contained. It explains the macro-to-micro reconstruction workflow, node semantics, relation directions, evidence rules, source anchors, and expected outputs. It also links to the canonical schema and the full Agent Skill for agents that can load additional resources.

A URL is **not** the same thing as an installed Agent Skill. The formal Agent Skills format still uses a `SKILL.md` directory. The zero-install entry point is a portable instruction protocol for agents with web-reading capability.

## Minimal prompt

```text
Read and follow the Discourse Atlas protocol:
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/AGENT.md

Analyze this source:
<SOURCE URL OR ATTACHED DOCUMENT>

Start with a readable work-level argument map. Identify the main claim and argumentative role of each major part/chapter, then recursively expand to section and local-argument level only where useful. Preserve authorial headings, mark inferred structure, ground major relations in evidence, and return canonical Discourse Atlas JSON when possible.
```

## Expected result

The agent should produce a progressive hierarchy rather than one flat graph:

```text
work
└── part / chapter
    └── section
        └── local argument unit
```

At each useful node the reconstruction distinguishes:

- `title` — what the textual unit is called;
- `main_claim` — what proposition it advances, when it advances one;
- `summary` — what it discusses or does;
- `function` — its discourse function;
- `role_in_parent` — why it is needed at the next higher level.

Logical/discourse edges remain separate from containment.

## Why the macro view comes first

A long book may contain hundreds of useful local units. Showing them all at once produces an unreadable graph. Discourse Atlas therefore treats visualization as progressive disclosure:

```text
Work Map -> Chapter Map -> Section Map -> Local Argument Map
```

The work map should answer, at a glance:

1. What problem is the work addressing?
2. What is the central thesis or target conclusion?
3. Which major parts establish which claims?
4. Why is each part needed?
5. Which major parts support, require, refine, challenge, or respond to others?

The reader can then drill down into a chapter or section without losing the global architecture.

## Source-access boundary

The protocol does not grant an agent access to a source it cannot already read. If an online document is blocked, private, paywalled, or otherwise inaccessible to the agent, provide the text/file through the agent's normal file or connector mechanism.

The agent should never reconstruct inaccessible text from titles, snippets, or guesses.

## Formal Skill path

Agents that support the Agent Skills standard can instead install or load:

```text
skills/discourse-structure/
```

The formal Skill and the remote protocol are two entry points to the same methodology. The canonical JSON schema remains the interoperability layer between agents, validators, evaluation tools, and the viewer.
