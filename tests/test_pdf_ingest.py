import json
from hashlib import sha256
from pathlib import Path

from pypdf import PdfWriter

from discourse_atlas.cli import main
from discourse_atlas.pdf_ingest import PAGE_SEPARATOR, build_paged_source, ingest_pdf


def write_blank_pdf(path: Path, pages: int = 2) -> None:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with path.open("wb") as handle:
        writer.write(handle)


def test_build_paged_source_tracks_unicode_code_points_and_empty_pages():
    text, manifest = build_paged_source(["第一页🙂", "", "Third"], source_name="sample.pdf", source_sha256="a" * 64)

    assert text == f"第一页🙂{PAGE_SEPARATOR}{PAGE_SEPARATOR}Third"
    assert len("第一页🙂") == 4
    assert manifest["page_count"] == 3
    assert manifest["empty_page_count"] == 1
    assert manifest["char_offset_unit"] == "unicode_code_point"
    assert manifest["pages"] == [
        {"page": 1, "char_start": 0, "char_end": 4, "empty": False},
        {"page": 2, "char_start": 7, "char_end": 7, "empty": True},
        {"page": 3, "char_start": 10, "char_end": 15, "empty": False},
    ]
    assert manifest["text_char_count"] == 15


def test_ingest_blank_pdf_records_hash_and_empty_pages(tmp_path):
    pdf = tmp_path / "blank.pdf"
    write_blank_pdf(pdf)

    text, manifest = ingest_pdf(pdf)

    assert text == PAGE_SEPARATOR
    assert manifest["page_count"] == 2
    assert manifest["empty_page_count"] == 2
    assert manifest["source_name"] == "blank.pdf"
    assert manifest["source_sha256"] == sha256(pdf.read_bytes()).hexdigest()
    assert manifest["pages"][0]["char_start"] == 0
    assert manifest["pages"][0]["char_end"] == 0
    assert manifest["pages"][1]["char_start"] == len(PAGE_SEPARATOR)


def test_ingest_pdf_cli_writes_defaults_and_refuses_overwrite(tmp_path, capsys):
    pdf = tmp_path / "input.pdf"
    write_blank_pdf(pdf)

    assert main(["ingest-pdf", str(pdf)]) == 0
    text_path = tmp_path / "input.txt"
    manifest_path = tmp_path / "input.pages.json"
    assert text_path.read_text(encoding="utf-8") == PAGE_SEPARATOR
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["page_count"] == 2
    assert "OCR is not performed" in capsys.readouterr().err

    assert main(["ingest-pdf", str(pdf)]) == 2
    assert "use --force to overwrite" in capsys.readouterr().err

    assert main(["ingest-pdf", str(pdf), "--force"]) == 0


def test_ingest_pdf_cli_rejects_same_text_and_manifest_path(tmp_path, capsys):
    pdf = tmp_path / "input.pdf"
    write_blank_pdf(pdf, pages=1)
    same = tmp_path / "same.out"

    assert main(["ingest-pdf", str(pdf), "-o", str(same), "--manifest", str(same)]) == 2
    assert "must be different" in capsys.readouterr().err


def test_malformed_pdf_returns_controlled_cli_error_without_outputs(tmp_path, capsys):
    pdf = tmp_path / "broken.pdf"
    pdf.write_bytes(b"not a pdf")

    assert main(["ingest-pdf", str(pdf)]) == 1
    assert "PDF ingestion failed" in capsys.readouterr().err
    assert not (tmp_path / "broken.txt").exists()
    assert not (tmp_path / "broken.pages.json").exists()
