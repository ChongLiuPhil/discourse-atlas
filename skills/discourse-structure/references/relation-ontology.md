# Relation Ontology (MVP)

Keep the ontology small and stable. Add an edge only when it carries explanatory value.

## Direction rule

An edge is always written:

`source --relation--> target`

## Relations

### `requires`

**Meaning:** source is a prerequisite for adequately understanding, motivating, or establishing target.

**Direction:** prerequisite → dependent.

Positive example: a conceptual distinction introduced in §2 is required by the argument in §4.

False positive: §2 merely appears before §4.

### `supports`

**Meaning:** source provides a reason, consideration, evidence, or argumentative basis for target.

**Direction:** support → supported unit.

False positive: two units reach compatible conclusions without one supplying support for the other.

### `derives`

**Meaning:** target is explicitly or strongly developed as a consequence, extension, or derivation from source.

**Direction:** basis → derived unit.

Use when the text presents a stronger developmental relation than generic support.

### `refines`

**Meaning:** source makes the target more precise, qualified, restricted, or articulated.

**Direction:** refining unit → refined unit.

The edge explanation must state what is being refined.

### `contrasts`

**Meaning:** source is deliberately set against target to expose a difference in concept, method, position, or consequence.

**Direction:** source → target; direction is usually organizational rather than asymmetric in content.

Use sparingly.

### `objects_to`

**Meaning:** source raises a criticism, counterexample, tension, or objection against target.

**Direction:** objection → target.

### `responds_to`

**Meaning:** source answers an objection, question, tension, or problem represented by target.

**Direction:** response → objection/problem.

### `illustrates`

**Meaning:** source provides an example, case, application, analogy, or concrete instantiation of target.

**Direction:** example/application → general point.

### `sequence`

**Meaning:** source precedes target in a meaningful textual progression, but no stronger logical dependency is justified.

**Direction:** earlier → later.

This is the fallback relation for useful organization when dependency would overstate the evidence. Never describe `sequence` as logical necessity.

## Choosing among relations

Prefer the strongest relation that is clearly supported, but not stronger.

- prerequisite but not evidential support → `requires`
- reason/evidence → `supports`
- explicit developmental consequence → `derives`
- qualification / specification → `refines`
- criticism → `objects_to`
- answer to criticism/problem → `responds_to`
- example/application → `illustrates`
- mere meaningful progression → `sequence`

Do not add multiple near-duplicate edges between the same nodes unless they capture genuinely distinct relations.
