from __future__ import annotations

from hashlib import sha256
from pathlib import Path

PAGE_SEPARATOR = "\n\f\n"
MANIFEST_VERSION = "0.1.0"


class PdfDependencyError(RuntimeError):
    """Raised when the optional PDF dependency is unavailable."""


class PdfIngestionError(ValueError):
    """Raised when a PDF cannot be parsed or its text layer cannot be extracted."""


def _normalize_page_text(text: str | None) -> str:
    if not text:
        return ""
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def build_paged_source(
    page_texts: list[str | None],
    *,
    source_name: str | None = None,
    source_sha256: str | None = None,
) -> tuple[str, dict]:
    """Build form-feed-delimited text plus an exact Unicode code-point page manifest."""
    normalized = [_normalize_page_text(text) for text in page_texts]
    chunks: list[str] = []
    pages: list[dict] = []
    cursor = 0

    for index, text in enumerate(normalized, start=1):
        if index > 1:
            chunks.append(PAGE_SEPARATOR)
            cursor += len(PAGE_SEPARATOR)
        start = cursor
        chunks.append(text)
        cursor += len(text)
        pages.append(
            {
                "page": index,
                "char_start": start,
                "char_end": cursor,
                "empty": not bool(text),
            }
        )

    source_text = "".join(chunks)
    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "format": "discourse-atlas-paged-source",
        "char_offset_unit": "unicode_code_point",
        "page_separator": PAGE_SEPARATOR,
        "page_count": len(pages),
        "empty_page_count": sum(page["empty"] for page in pages),
        "source_name": source_name,
        "source_sha256": source_sha256,
        "text_char_count": len(source_text),
        "pages": pages,
    }
    return source_text, manifest


def extract_pdf_pages(path: str | Path) -> list[str]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - exercised in normal installs without the extra
        raise PdfDependencyError(
            "PDF ingestion requires the optional dependency: pip install 'discourse-atlas[pdf]'"
        ) from exc

    pdf_path = Path(path)
    try:
        reader = PdfReader(str(pdf_path))
        if reader.is_encrypted:
            try:
                result = reader.decrypt("")
            except Exception as exc:
                raise PdfIngestionError("encrypted PDF could not be opened without a password") from exc
            if result == 0:
                raise PdfIngestionError(
                    "encrypted PDF requires a password; password-based ingestion is not supported"
                )

        pages: list[str] = []
        for page_number, page in enumerate(reader.pages, start=1):
            try:
                pages.append(page.extract_text() or "")
            except Exception as exc:
                raise PdfIngestionError(
                    f"text extraction failed on page {page_number}: {exc}"
                ) from exc
        return pages
    except PdfIngestionError:
        raise
    except Exception as exc:
        raise PdfIngestionError(f"PDF ingestion failed: {exc}") from exc


def ingest_pdf(path: str | Path) -> tuple[str, dict]:
    pdf_path = Path(path)
    digest = sha256(pdf_path.read_bytes()).hexdigest()
    pages = extract_pdf_pages(pdf_path)
    return build_paged_source(
        pages,
        source_name=pdf_path.name,
        source_sha256=digest,
    )
