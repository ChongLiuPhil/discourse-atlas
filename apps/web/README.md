# Discourse Atlas Web

Interactive reader for Discourse Atlas JSON graphs.

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
npm install
npm test
npm run dev
```

`npm run prepare:data` copies the canonical mini-essay example from the repository root into `public/`; the web app does not maintain a second hand-edited example.

## Build

```bash
npm run build
```

The output is a static Vite site in `apps/web/dist/`. `base: './'` keeps the build portable to a subpath such as GitHub Pages.
