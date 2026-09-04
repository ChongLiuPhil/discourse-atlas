# Unit alignment

Discourse Atlas v0.5 separates **unit alignment** from **structural evaluation**. This is necessary because two reconstructions may refer to the same textual material while using different node IDs or different segmentation.

## Why alignment is explicit

A hidden embedding matcher would mix two questions:

1. Which textual units correspond?
2. Given that correspondence, are the hierarchy, discourse relations, and evidence claims similar?

Discourse Atlas keeps these questions separate. An alignment is a reviewable JSON artifact.

## Alignment units

Each alignment unit maps one or more reference nodes to one or more candidate nodes:

```json
{
  "unit_id": "u-fallibility",
  "reference_node_ids": ["frame", "fallibility"],
  "candidate_node_ids": ["fallibility-case"],
  "method": "manual-split-merge",
  "confidence": 0.98,
  "status": "accepted",
  "rationale": "One reconstruction separates framing from the first branch; the other combines them."
}
```

This representation supports one-to-one, one-to-many, many-to-one, and many-to-many correspondences without rewriting either graph.

## Deterministic proposals

```bash
discourse-atlas align reference.json candidate.json -o alignment.json
```

The proposer uses, in order:

1. work-root compatibility;
2. stable identical node IDs;
3. Jaccard overlap of source anchor coordinates (paragraphs, then lines, then section labels as a fallback).

It is intentionally not called semantic truth. The output uses `status: proposed` and can be reviewed or edited. Automatic proposals are currently one-to-one; split/merge units must be made explicit by a reviewer.

## Evaluation after alignment

```bash
discourse-atlas evaluate reference.json candidate.json --alignment alignment.json
```

Nodes inside the same alignment unit are collapsed for comparison. Relations whose endpoints collapse into the same unit are treated as internal segmentation detail and excluded from inter-unit relation scoring. Node and edge evidence are compared using source coordinates rather than anchor IDs.

## Multiple references

```bash
discourse-atlas multi-evaluate candidate.json ref-a.json ref-b.json --auto-align
```

The report includes every per-reference result, the best reference, mean score, and score range. A high best-reference score therefore means “the candidate closely matches at least one accepted reconstruction,” not “the candidate discovered the uniquely true graph.”

For reviewed split/merge mappings, pass explicit per-reference files with repeated `--alignment-map REFERENCE=ALIGNMENT_JSON` arguments.
