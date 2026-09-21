# Current AHICP / Inquiry Publishing Stack Adoption — Discourse Atlas

Discourse Atlas adopts current AHICP as a thin adapter over its existing repository-native product governance. The adoption does not replace the Manifest, Context Interface, Project Status, Decision Records, schemas, ontology, release process, or product protocol.

## Stack v2 revisions

- AHICP template: `02d0b3c02ca23073c760b6e0f761a468e0235a1c`; project adopted: `ed5a60b1016497472072db108072ace59bcdb65d`
- PPF template: `9a6005de85f032095e36eea03fda317e73126538`; project adopted: `e660b48fb216c28c8faa1f0fe2d0816401e1de2c`
- Vault template: `592c6e2e938f995b7b3e7df07a72f7f1e2c50c5a`; project adopted: `79d64b12275a5cc7c09236b144bf4213fa7afc5e`
- Starter source revision: `05857086e240cbd269eae91af8419ea0921c01fa`

## Functional mapping

| Stack role | Project-native authority |
| --- | --- |
| Repository routing | `PROJECT_MANIFEST.yaml` |
| Context routing | `PROJECT_CONTEXT_INTERFACE.yaml` |
| Operational resume | `PROJECT_STATUS.md` |
| Decision authority/history | `GOVERNANCE.md` + `docs/decisions/` |
| Product protocol | `AGENT.md` + `skills/discourse-structure/` |
| Semantic authority | versioned schemas + relation ontology + canonical references |
| Release/version authority | `docs/versioning.md` + `docs/release-process.md` |
| Web production | `apps/web/` + `.github/workflows/pages.yml` |

AHICP uses a project-specific product-governance functional mapping. No duplicate Content Core, Form Core, research Framework Status, Argument Map, or full Working Memory tree is created.

## Publication mapping

The Hosted Interactive Atlas is already authorized and public:

- repository: public
- provider: GitHub Pages
- production URL: `https://chongliuphil.github.io/discourse-atlas/`
- source: GitHub Actions
- integration state: production active
- main deployment: automatic
- post-deploy endpoint verification: active

`website.yaml publish=false` is a separate Academic Vault / homepage-change boundary. It does not revoke or contradict the existing public Hosted Atlas.

Toolkit/version release semantics remain controlled by `docs/release-process.md`; a routine Pages deployment is not by itself a new toolkit release.
