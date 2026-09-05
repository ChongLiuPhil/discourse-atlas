---
name: discourse-structure
description: Reconstruct the hierarchical structure, section functions, and logical/discourse dependencies of argumentative or expository texts. Use for essays, philosophy, academic papers, theoretical books, legal reasoning, policy reports, and similar works when the user wants more than a summary: chapter/section architecture, inferred segmentation where necessary, dependency relations, argument flow, or an evidence-anchored structural map.
license: MIT
compatibility: Requires access to the source text. Produces portable JSON and Markdown; no vendor-specific API is required.
---

# Discourse Structure Reconstruction

Reconstruct a text as a **hierarchical discourse graph**, not merely as a summary or list of claims.

The output has two distinct structures:

1. **Containment hierarchy**: work → part → chapter → section → subsection → paragraph / argument unit.
2. **Logical/discourse dependency graph**: directed relations among those units.

Never collapse these into one tree.

## Required outputs

Produce both:

- `analysis.json`, conforming to `../../schemas/discourse-graph.schema.json` when that schema is available to the agent; and
- `analysis.md`, a readable reconstruction with hierarchy, functions, major dependencies, evidence, and uncertainty.

If file output is unavailable, emit the JSON and Markdown in clearly separated sections.

## Governing principles

1. **Structure before summary.** Recover architecture before writing global conclusions.
2. **Preserve authorial structure.** Existing author-provided headings outrank inferred segmentation.
3. **Never disguise inferred headings as authorial headings.** Mark every inferred node with `structure_origin: inferred`.
4. **Separate sequence from dependence.** A before B in the text does not imply B logically depends on A.
5. **Evidence important relations.** Major inferred edges need source anchors and a short explanation.
6. **Prefer sparse, defensible graphs.** Do not add an edge merely because two sections are adjacent or topically related.
7. **Represent uncertainty.** Use confidence and assertion level rather than pretending every reconstruction is certain.
8. **Allow non-tree logic.** Cross-chapter and cross-level edges are permitted. Do not force the dependency graph to be acyclic.
9. **Reconstruction, not revelation.** Treat the graph as a reasoned interpretation that a reader may revise.

## Workflow

### Pass 0 — prepare the accessible source

Use the most reproducible source representation actually available.

- If the supplied source is already stable text/Markdown, analyze it directly.
- If the supplied source is a PDF and Discourse Atlas PDF ingestion tooling is available, follow `references/pdf-ingestion.md` to extract its text layer into page-delimited Unicode text before analysis.
- Never silently substitute OCR for text-layer extraction. If scanned/image-only pages are unavailable as text, preserve that limitation rather than inventing content.

### Pass 1 — recover textual hierarchy

Read the whole available structure before inferring relations.

- Detect explicit parts, chapters, sections, subsection labels, numbered divisions, typographic headings, and author-provided transitions.
- Preserve explicit units exactly enough to remain recognizable.
- If the source lacks usable segmentation, infer the smallest useful hierarchy following `references/segmentation-rules.md`.
- If only some regions lack headings, infer structure only in those regions.

### Pass 2 — analyze leaf units

For every leaf section or smallest useful unit, record:

- a concise summary;
- one or more discourse functions (for example: `defines`, `distinguishes`, `motivates`, `argues`, `objects`, `responds`, `illustrates`, `synthesizes`, `concludes`);
- its role within its parent;
- source anchors;
- confidence.

For source anchors, follow `references/source-anchors.md`. Preserve paragraph/line coordinates when available; add page coordinates only for the supplied page-bearing source or edition; add exact Unicode code-point character ranges only when they are genuinely available. Never invent page numbers or exact offsets.

Do not use function labels as logical edges automatically.

### Pass 3 — infer sibling relations

Within each parent, inspect sibling units as a set.

Ask:

- Does a later unit require a distinction, result, or premise established earlier?
- Does one unit support, refine, contrast with, object to, or respond to another?
- Is the relation merely chronological/textual sequence?

Use the ontology in `references/relation-ontology.md`.

### Pass 4 — synthesize parent units

After leaf relations are stable, summarize each parent unit by the function of its children.

Infer parent-to-parent relations only when the relation is supported by the functions and content of the children. Do not infer a chapter edge solely because one chapter follows another.

### Pass 5 — search for cross-hierarchy dependencies

Look for important relations that skip the local hierarchy, for example:

- Chapter 4 relies directly on a distinction introduced in Section 1.3.
- A late objection targets a thesis introduced several chapters earlier.
- An example in one part illustrates a framework established in another.

Add only relations that improve understanding of the work's architecture.

### Pass 6 — evidence and uncertainty audit

For every major edge:

- verify source and target exist;
- verify direction under the ontology;
- give a one-sentence explanation;
- attach evidence anchors where possible;
- set confidence in `[0,1]`;
- label assertion level as `explicit`, `strongly_inferred`, or `tentative`.

Delete weak decorative edges. Before finalizing JSON, also verify that every referenced node and anchor exists, node/edge/anchor IDs are unique, source anchor ranges are internally consistent, and the containment hierarchy has exactly one `work` root with no containment cycles.

### Pass 7 — global reconstruction

Write a short account of the whole work's architecture:

- What problem or task launches the text?
- What conceptual prerequisites are established?
- What are the major transitions?
- Where do objections, revisions, applications, or conclusions enter?
- Which dependencies are global rather than local?

This should explain the **logic of the composition**, not repeat section summaries.

## Output conventions

### `analysis.json`

Use stable node and edge IDs. Prefer readable identifiers such as:

- `ch-1`
- `sec-1-2`
- `edge-sec-1-2--sec-2-1`

For inferred headings, title them descriptively but conservatively. Do not imitate the author's voice.

### `analysis.md`

Use this order:

1. `# Structural Reconstruction`
2. `## Global Architecture`
3. `## Hierarchy`
4. `## Major Logical Dependencies`
5. `## Cross-Hierarchy Relations`
6. `## Uncertain or Alternative Readings`

For each major edge, include source → relation → target, explanation, evidence anchor(s), and confidence.

## Quality checks

Before finishing, verify:

- authorial and inferred structures are visibly distinguishable;
- every node except the root has a valid parent if a parent is claimed;
- edge endpoints exist;
- source preparation is explicit and does not conceal OCR or extraction gaps;
- source anchors use only coordinates supported by the supplied source and obey `references/source-anchors.md`;
- `requires` direction means prerequisite → dependent;
- `supports` direction means supporting unit → supported unit;
- `objects_to` direction means objection → target;
- `responds_to` direction means response → objection/problem;
- `sequence` is not presented as logical necessity;
- the graph is readable at work, chapter, and section scales;
- the global account explains why the author needs the major stages of the text.
