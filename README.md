# Discourse Atlas

**Discourse Atlas** is an open-source, agent-skill-first toolkit for reconstructing the hierarchical structure and logical dependencies of argumentative and expository texts.

It is designed for essays, philosophy, academic papers, theoretical books, legal reasoning, policy reports, and other texts where understanding **how the parts depend on one another** matters as much as understanding what each part says.

> Status: functional v0.4 research preview: analysis skill, validator, interactive reader, and evaluation toolkit.

## Core idea

Discourse Atlas models a text as two related structures:

1. **Containment hierarchy** — work → part → chapter → section → paragraph / argument unit.
2. **Discourse dependency graph** — relations such as `requires`, `supports`, `derives`, `refines`, `objects_to`, and `responds_to`.

The canonical representation is JSON. Visualizations are derived views, not the source of truth.

## Design principles

- **Structure before summary.** Recover the architecture of the text before summarizing it.
- **Preserve authorial structure.** If the author provides chapters or sections, retain them.
- **Mark inferred structure explicitly.** AI-generated sections must never be presented as authorial headings.
- **Separate hierarchy from dependency.** Containment is not the same as logical dependence.
- **Evidence for important edges.** Major inferred relations should point back to source anchors.
- **Reconstruction, not revelation.** The output is a criticizable interpretation, not a claim to the single true structure of a text.

## Repository layout

```text
discourse-atlas/
├── skills/discourse-structure/   # Portable Agent Skill
├── schemas/                      # Canonical JSON Schema
├── src/discourse_atlas/          # Validation + render CLI
├── apps/web/                     # Interactive React Flow + ELK reader
├── examples/mini-essay/          # Small end-to-end example
├── tests/                        # Schema / renderer tests
├── docs/                         # Architecture notes
└── .github/workflows/            # CI
```

## Use as an Agent Skill

Copy `skills/discourse-structure/` into a client that supports the Agent Skills `SKILL.md` format. Ask the agent to analyze a text's discourse structure and produce:

- `analysis.json` — machine-readable graph
- `analysis.md` — human-readable reconstruction

The skill is intentionally model- and vendor-neutral.

## CLI

The small Python package validates analysis files at both the JSON-Schema and graph-reference levels, then exports lightweight diagram formats.

```bash
python -m pip install -e '.[dev]'  # development checkout

discourse-atlas validate examples/mini-essay/analysis.json
discourse-atlas mermaid examples/mini-essay/analysis.json
discourse-atlas dot examples/mini-essay/analysis.json
discourse-atlas evaluate benchmark/cases/mini-essay/gold.json candidate.json
discourse-atlas agreement annotation-a.json annotation-b.json
```

Validation also checks unique IDs, parent references, containment cycles, edge endpoints, evidence anchors, and anchor ranges. The JSON graph remains canonical; Mermaid and Graphviz DOT are convenience exports.

## Interactive reader

The web app in `apps/web/` turns the canonical JSON graph into a synchronized reading environment. It uses nested React Flow nodes for containment and ELK layered layout for directional dependencies, while keeping renderer state outside the canonical schema.

```bash
cd apps/web
npm install
npm run dev
```

Open a Discourse Atlas `analysis.json`, optionally load its source Markdown/text, inspect evidence by clicking graph relations, click source passages to trace which structural claims use them, edit the reconstruction in the inspector, and export a corrected JSON file.

## Relation ontology (MVP)

| Relation | Meaning |
|---|---|
| `requires` | source is a prerequisite for understanding or establishing target |
| `supports` | source gives reasons/evidence for target |
| `derives` | target is developed or derived from source |
| `refines` | source makes target more precise, qualified, restricted, or articulated |
| `contrasts` | source and target are deliberately contrasted |
| `objects_to` | source raises an objection to target |
| `responds_to` | source answers a problem or objection in target |
| `illustrates` | source exemplifies or applies target |
| `sequence` | textual/organizational order only; not logical dependence |

See `skills/discourse-structure/references/relation-ontology.md` for direction rules.

## Example

The bundled mini essay has three inferred sections:

```text
Problem framing → Conceptual distinction → Conclusion
                         └──────── supports ────────→
```

The example demonstrates the difference between an inferred hierarchy and a logical edge.

## Roadmap

### v0.1 — specification-first MVP
- [x] Portable `SKILL.md`
- [x] JSON Schema
- [x] Relation ontology
- [x] Segmentation rules
- [x] Example analysis
- [x] Validator + Mermaid/DOT exporters

### v0.2 — interactive map
- [x] React Flow viewer
- [x] ELK hierarchical layout
- [x] Collapsible nested sections
- [x] Edge evidence inspector

### v0.3 — synchronized reading
- [x] Source text + map side-by-side
- [x] Click graph node → jump to text
- [x] Select source passage → highlight relevant graph nodes/edges
- [x] Human correction workflow + JSON export

### v0.4 — evaluation
- [x] Benchmark protocol + synthetic smoke-test corpus
- [x] Human inter-annotator comparison command
- [x] Structural fidelity metrics
- [x] Relation and evidence precision / recall metrics

### Beyond v0.4
- [ ] Larger reviewed public-domain / permission-compatible benchmark corpus
- [ ] Semantic unit alignment for unconstrained model outputs
- [ ] Multi-reference scoring for alternative defensible reconstructions
- [ ] Optional hosted demo / GitHub Pages deployment

## Evaluation

The evaluation layer is intentionally explicit about interpretive plurality. Exact-ID metrics are used only after textual units have been aligned; the CLI reports hierarchy accuracy, relation precision/recall/F1, node-anchor grounding, edge-evidence grounding, and symmetric inter-annotator agreement. See `benchmark/README.md` and `docs/evaluation.md`.

## Non-goals

Discourse Atlas is not intended to:

- replace close reading;
- claim that a philosophical text has one uniquely correct formal structure;
- flatten every relation into premise/conclusion pairs;
- treat textual order as logical dependence by default.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Early contributions are especially useful in ontology design, evaluation methodology, visualization, and philosophy / humanities test cases.

## License

MIT. See [LICENSE](LICENSE).
