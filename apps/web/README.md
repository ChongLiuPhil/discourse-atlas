# Discourse Atlas Web

Interactive reader for Discourse Atlas JSON graphs.

Hosted app: <https://chongliuphil.github.io/discourse-atlas/>

## Features

- nested work / part / chapter / section containers;
- ELK layered layout with cross-hierarchy dependency edges;
- collapse / expand of compound sections;
- source-text synchronization for paragraph and line anchors;
- node and edge evidence inspection;
- source passage → graph highlighting;
- human correction of node and relation metadata;
- export of the corrected canonical JSON graph;
- local loading of another analysis JSON and source Markdown/text file.

## Development

Requires Node.js 20.19+ or 22.12+ (Vite 8 requirement).

```bash
cd apps/web
npm ci
npm test
npm run dev
```

Use `npm install` instead of `npm ci` only when intentionally changing dependency declarations/lock state.

`npm run prepare:data` copies the canonical mini-essay example from the repository root into `public/`; the web app does not maintain a second hand-edited example.

## Build

```bash
npm run build
```

The output is a static Vite site in `apps/web/dist/`. Production builds use `base: '/discourse-atlas/'` so generated assets resolve correctly from the repository-scoped GitHub Pages URL.

GitHub Pages deployment is defined in `.github/workflows/pages.yml` and publishes `apps/web/dist/` through the GitHub Pages Actions artifact/deployment flow.
