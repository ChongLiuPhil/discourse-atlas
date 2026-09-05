# Source anchor conventions

Use source anchors to make structural claims inspectable. Prefer coordinates that the supplied source actually supports; never invent pagination or character positions.

## Coordinate systems

Discourse Atlas supports these optional anchor coordinates:

- `paragraph_start` / `paragraph_end`: 1-based, inclusive;
- `line_start` / `line_end`: 1-based, inclusive;
- `page_start` / `page_end`: 1-based, inclusive, tied to the supplied edition or PDF;
- `char_start`: 0-based, inclusive Unicode code-point offset;
- `char_end`: 0-based, exclusive Unicode code-point offset.

Character offsets count Unicode code points, not UTF-8 bytes and not JavaScript UTF-16 code units. For example, an emoji counts as one code point.

## Selection policy

1. Preserve paragraph and line coordinates when the source already provides a stable text representation.
2. Add page coordinates when the source is page-bearing (PDF, scanned edition, fixed scholarly edition) and the page numbers are known from that exact source.
3. Add character coordinates when exact machine-readable spans are available and useful for synchronization or evaluation.
4. Multiple coordinate systems may coexist on one anchor. They should identify the same source span.
5. Do not infer a page number from an unrelated edition or a web transcription.
6. Do not fabricate exact character offsets from approximate quotations.

## Range rules

For paragraph, line, and page ranges, the start may equal the end. An omitted end means a one-unit span.

For character ranges, both endpoints should be present and `char_start < char_end`. The end is exclusive so adjacent spans can be represented without overlap.

## Alignment priority

When automatic deterministic alignment compares anchors, it uses:

1. paragraph/line coordinates when present;
2. character coordinates otherwise;
3. page coordinates otherwise;
4. `section_label` as a final fallback.

Character overlap is scored with fixed 32-code-point cells for scalability; the stored anchor coordinates themselves remain exact.

Automatic alignment is only a proposal. Split/merge or edition-sensitive correspondences should be explicitly reviewed.
