# PDF text ingestion

Discourse Atlas v0.8 adds an explicit PDF **text-layer ingestion** step. It converts a PDF into the page-aware Unicode source format consumed by the v0.7 scholarly-anchor model.

## Install

PDF support is optional so the core package remains lightweight:

```bash
pip install 'discourse-atlas[pdf]'
```

The PDF extra uses `pypdf` 6.x. Development installs include the same dependency so ingestion is exercised in CI.

## Command

```bash
discourse-atlas ingest-pdf book.pdf
```

By default this writes:

- `book.txt` — extracted Unicode text with `\n\f\n` between PDF pages;
- `book.pages.json` — a provenance and page-coordinate manifest.

Custom paths are supported:

```bash
discourse-atlas ingest-pdf book.pdf -o source.txt --manifest source.pages.json
```

Existing outputs are not overwritten unless `--force` is supplied.

## Manifest

The page manifest records:

- manifest format/version;
- source PDF filename;
- SHA-256 of the PDF bytes;
- `unicode_code_point` as the character-offset unit;
- the exact page separator;
- total and empty page counts;
- total emitted-text character count;
- for each PDF page: 1-based page number, 0-based inclusive `char_start`, 0-based exclusive `char_end`, and whether the extracted page was empty.

The page separators are part of the emitted source text and therefore contribute to later-page character offsets. This makes page/character coordinates reproducible from the emitted text alone.

## Normalization

For each extracted page, Discourse Atlas:

1. normalizes CRLF/CR newlines to LF;
2. strips leading/trailing whitespace around the whole page;
3. preserves the remaining extracted text as returned by the PDF text layer;
4. joins pages using the fixed `\n\f\n` separator.

This is deliberately conservative. It does not attempt layout reconstruction, column reordering beyond what the PDF extractor returns, dehyphenation, quotation correction, or semantic cleanup.

## OCR boundary

`ingest-pdf` does **not** perform OCR. A scanned/image-only page normally yields an empty page span and is counted in `empty_page_count`; the CLI warns when any page yields no text.

This distinction is intentional: text extraction and OCR introduce different evidence/provenance risks. A future OCR adapter should be explicit and should preserve its own provenance rather than silently changing the source text.

## Encryption and failures

Password-protected PDFs that cannot be opened with an empty password are rejected; password-based ingestion is not supported in v0.8. Malformed PDFs and page-level extraction failures return controlled CLI errors rather than partial output.

## Relationship to discourse anchors

The ingestion manifest is source-preparation metadata, not an `analysis.json` graph. Agents or annotation tooling may use the emitted page boundaries and exact character ranges when creating `page_start/page_end` and `char_start/char_end` source anchors.

The synchronized reader already understands form-feed page boundaries, so `book.txt` can be loaded directly alongside a compatible discourse graph.
