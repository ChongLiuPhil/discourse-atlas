# Scholarly source anchors

Discourse Atlas v0.7 adds page and character coordinates to the existing paragraph/line anchor model so reconstructions can remain grounded in fixed editions, PDF-derived text, and exact machine-readable spans.

## Coordinate semantics

| Field | Base | End semantics | Intended use |
|---|---:|---|---|
| `paragraph_start` / `paragraph_end` | 1 | inclusive | stable paragraph-numbered text |
| `line_start` / `line_end` | 1 | inclusive | line-addressable source text |
| `page_start` / `page_end` | 1 | inclusive | PDFs and fixed scholarly editions |
| `char_start` | 0 | inclusive | exact Unicode code-point span |
| `char_end` | 0 | exclusive | exact Unicode code-point span |

Character offsets count Unicode code points. They are not UTF-8 byte offsets and not JavaScript UTF-16 code-unit indexes. This makes Python and browser behavior consistent for Chinese, emoji, and other non-BMP characters.

The canonical graph schema stays at `0.1.0` because these fields are optional and backward compatible.

## Validation

The validator enforces:

- page, paragraph, and line starts must not exceed their ends;
- an end coordinate cannot exist without its corresponding start;
- a character span must satisfy `char_start < char_end`;
- schema minima remain page/paragraph/line ≥ 1 and character offsets ≥ 0.

The validator does not check whether `char_end` exceeds a particular source file length because graph validation may occur without the source text.

## Deterministic alignment

Automatic alignment remains inspectable and non-semantic. For each anchor it prefers:

1. paragraph and line coordinates, preserving v0.5 behavior;
2. character coordinates if paragraph/line coordinates are absent;
3. page coordinates if finer coordinates are absent;
4. `section_label` as a final fallback.

Character overlap uses 32-code-point cells to keep footprints bounded for long works. The stored raw offsets remain exact. This quantization affects proposal/evaluation overlap only; it does not alter source navigation.

Page numbers are edition-specific. Page-only automatic alignment is therefore appropriate only when both reconstructions address the same edition/source. Cross-edition correspondences should be reviewed explicitly.

## Web reader

The synchronized reader records each displayed source block with:

- paragraph number;
- source line range;
- Unicode code-point character range;
- page range when form-feed (`\f`) page boundaries are present in extracted text.

A focused anchor is resolved in the same priority order: paragraph, line, character, then page. Character anchors therefore work in ordinary text/Markdown sources, while page-only navigation works for text extractions that preserve page breaks with form-feed separators.

The Inspector displays available coordinate labels alongside each anchor ID.

## PDF workflow boundary

v0.7 defines and consumes page-aware coordinates but does not itself perform PDF extraction or OCR. A PDF ingestion layer may supply page-numbered/character-addressable text later without changing the canonical graph representation.
