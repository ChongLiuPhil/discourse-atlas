# Alignment workbench

Discourse Atlas v0.6 adds a browser-based adjudication surface for the explicit alignment format introduced in v0.5.

## Purpose

The workbench is not a semantic oracle. It lets a reviewer inspect and edit the correspondence assumptions that structural evaluation depends on.

Open the web app and switch from **Reader** to **Alignment**. The bundled example loads the two accepted reconstructions of the John Stuart Mill benchmark together with their reviewed split/merge alignment.

## Workflow

1. Load a reference reconstruction and a candidate reconstruction.
2. Optionally load an existing alignment or generate a deterministic anchor-overlap proposal.
3. Inspect proposed units and mark each as accepted, proposed, or rejected.
4. Rejected nodes become unmatched again and may be selected for a different correspondence.
5. Select one or more nodes on each side to create an explicit reviewed unit. Many-to-one and one-to-many units are recorded as `manual-split-merge`.
6. Add a rationale for interpretively significant correspondences.
7. Resolve duplicate/unknown membership errors.
8. Export `alignment.reviewed.json` and pass it to the CLI `evaluate` or `agreement` command.

## Browser proposal parity

The browser proposal model follows the same order as the Python CLI:

1. single work-root compatibility;
2. identical stable IDs;
3. greedy one-to-one Jaccard overlap over paragraph/line/section-label source coordinates.

It intentionally does not infer split/merge units automatically. Those require a reviewer to state the correspondence explicitly.

## Status semantics

- `proposed`: a suggestion that has not been adjudicated;
- `accepted`: an active reviewed correspondence used for coverage and export;
- `rejected`: retained for audit history but excluded from active node membership.

The workbench keeps rejected proposals visible so a later reader can see what was considered and declined.
