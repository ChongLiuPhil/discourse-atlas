# PDF source preparation

When the supplied source is a PDF and the environment provides Discourse Atlas PDF ingestion tooling, prefer the explicit text-layer ingestion step before reconstruction:

```bash
discourse-atlas ingest-pdf source.pdf
```

This produces page-delimited Unicode text plus a page/character manifest. Analyze the emitted text, and use page/character coordinates only when they can be grounded in that emitted source and manifest.

## Rules

1. Treat PDF text extraction as source preparation, not interpretation.
2. Preserve the PDF's page order.
3. Do not silently run OCR. Empty extracted pages must remain visible as an extraction limitation.
4. Do not invent text for scanned or unreadable pages.
5. Do not silently repair column order, hyphenation, quotations, headers, or footnotes if the extraction is uncertain; mention material extraction problems in the reconstruction notes.
6. Page coordinates refer to the supplied PDF's page sequence, not to page numbers from another edition.
7. Character coordinates refer to the exact emitted Unicode text and count Unicode code points.
8. Keep the PDF SHA-256/page manifest when reproducibility matters.

If PDF ingestion tooling is unavailable, work from whatever source representation is actually accessible and do not claim page/character precision that was not established.
