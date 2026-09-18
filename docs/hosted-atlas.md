# Hosted Interactive Atlas

Since Discourse Atlas v1.0, the browser reader and alignment workbench are published as a repository-scoped GitHub Pages site:

<https://chongliuphil.github.io/discourse-atlas/>

## What is hosted

The Pages site is the static Vite application from `apps/web/`. It includes the bundled mini-essay example and supports opening local Discourse Atlas analysis JSON plus source Markdown/text directly in the browser.

The hosted app does not replace the canonical JSON representation. It is a viewer and correction workspace for canonical Discourse Atlas data.

## Deployment

GitHub Pages is configured with **Source = GitHub Actions**. The deployment workflow is `.github/workflows/pages.yml`.

The workflow:

1. checks out the repository;
2. installs the web dependencies with Node.js 24;
3. runs the browser-model tests;
4. builds `apps/web/dist/`;
5. uploads the build as a Pages artifact;
6. deploys that artifact to the `github-pages` environment.

The Vite production base is `/discourse-atlas/`, matching the repository-scoped Pages URL. This is required so generated JavaScript, CSS, and other static assets resolve beneath `https://chongliuphil.github.io/discourse-atlas/` rather than from the domain root.

## Local verification

```bash
cd apps/web
npm install --no-audit --no-fund
npm test
npm run build
npm run preview
```

For release verification, confirm that the hosted URL loads without asset 404s, that the bundled example appears, that Reader/Alignment mode switching works, and that local analysis/source uploads remain available.
