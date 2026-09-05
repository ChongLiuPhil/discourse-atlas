from __future__ import annotations

import argparse
import json
import sys
from importlib import resources
from pathlib import Path

from jsonschema import Draft202012Validator

from .alignment import propose_alignment, validate_alignment
from .evaluation import (
    compare_annotations,
    compare_annotations_with_alignment,
    evaluate_against_references,
    evaluate_documents,
    evaluate_with_alignment,
)
from .pdf_ingest import PdfDependencyError, ingest_pdf
from .validation import validate_references


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_json(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def _schema() -> dict:
    repo_schema = _repo_root() / "schemas" / "discourse-graph.schema.json"
    if repo_schema.exists():
        return _load_json(repo_schema)
    packaged = resources.files("discourse_atlas.resources").joinpath("discourse-graph.schema.json")
    with packaged.open("r", encoding="utf-8") as f:
        return json.load(f)


def _alignment_schema() -> dict:
    repo_schema = _repo_root() / "schemas" / "node-alignment.schema.json"
    if repo_schema.exists():
        return _load_json(repo_schema)
    packaged = resources.files("discourse_atlas.resources").joinpath("node-alignment.schema.json")
    with packaged.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_document(document: dict) -> list[str]:
    validator = Draft202012Validator(_schema())
    schema_errors = sorted(validator.iter_errors(document), key=lambda e: list(e.path))
    errors = [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in schema_errors]
    if not schema_errors:
        errors.extend(validate_references(document))
    return errors


def _safe_mermaid(text: str) -> str:
    return text.replace('"', "'").replace("\n", " ")


def to_mermaid(document: dict) -> str:
    children: dict[str | None, list[dict]] = {}
    for node in document["nodes"]:
        children.setdefault(node.get("parent_id"), []).append(node)
    lines = ["flowchart TB"]

    def emit_group(parent_id: str | None, indent: int = 1) -> None:
        pad = "    " * indent
        for node in children.get(parent_id, []):
            node_id = node["id"]
            label = _safe_mermaid(node["title"])
            if children.get(node_id):
                lines.append(f'{pad}subgraph {node_id}["{label}"]')
                lines.append(f'{pad}    {node_id}_anchor((" "))')
                emit_group(node_id, indent + 1)
                lines.append(f"{pad}end")
            else:
                lines.append(f'{pad}{node_id}["{label}"]')

    emit_group(None)
    relation_labels = {
        "requires": "requires", "supports": "supports", "derives": "derives",
        "refines": "refines", "contrasts": "contrasts", "objects_to": "objects to",
        "responds_to": "responds to", "illustrates": "illustrates", "sequence": "sequence",
    }

    def endpoint(node_id: str) -> str:
        return f"{node_id}_anchor" if children.get(node_id) else node_id

    for edge in document.get("edges", []):
        source = endpoint(edge["source"])
        target = endpoint(edge["target"])
        label = relation_labels.get(edge["relation"], edge["relation"])
        lines.append(f'    {source} -->|"{label}"| {target}')
    return "\n".join(lines) + "\n"


def _dot_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def to_dot(document: dict) -> str:
    children: dict[str | None, list[dict]] = {}
    for node in document["nodes"]:
        children.setdefault(node.get("parent_id"), []).append(node)
    lines = ["digraph discourse_atlas {", "  rankdir=TB;", "  compound=true;", '  node [shape=box];']

    def emit(parent_id: str | None, indent: int = 1) -> None:
        pad = "  " * indent
        for node in children.get(parent_id, []):
            node_id = node["id"]
            title = _dot_escape(node["title"])
            if children.get(node_id):
                lines.append(f'{pad}subgraph "cluster_{node_id}" {{')
                lines.append(f'{pad}  label="{title}";')
                lines.append(f'{pad}  "{node_id}" [shape=point, width=0.01, label=""];')
                emit(node_id, indent + 1)
                lines.append(f"{pad}}}")
            else:
                lines.append(f'{pad}"{node_id}" [label="{title}"];')

    emit(None)
    for edge in document.get("edges", []):
        relation = _dot_escape(edge["relation"])
        lines.append(f'  "{edge["source"]}" -> "{edge["target"]}" [label="{relation}"];')
    lines.append("}")
    return "\n".join(lines) + "\n"


def validate_alignment_document(alignment: dict, reference: dict, candidate: dict) -> list[str]:
    validator = Draft202012Validator(_alignment_schema())
    schema_errors = sorted(validator.iter_errors(alignment), key=lambda e: list(e.path))
    errors = [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in schema_errors]
    if not schema_errors:
        errors.extend(validate_alignment(alignment, reference, candidate))
    return errors


def _write_or_print(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def _write_json(value: dict, output: str | None = None) -> None:
    _write_or_print(json.dumps(value, indent=2, sort_keys=True) + "\n", output)


def _validated_document(path: str, label: str) -> dict | None:
    document = _load_json(path)
    errors = validate_document(document)
    if errors:
        for error in errors:
            print(f"ERROR {label}: {error}", file=sys.stderr)
        return None
    return document


def _validated_pair(left_path: str, right_path: str) -> tuple[dict, dict] | None:
    left = _validated_document(left_path, "left/reference")
    right = _validated_document(right_path, "right/candidate")
    return (left, right) if left is not None and right is not None else None


def _parse_alignment_specs(values: list[str] | None) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for value in values or []:
        if "=" not in value:
            raise ValueError("--alignment-map entries must use REFERENCE=ALIGNMENT_JSON")
        reference, path = value.split("=", 1)
        result[reference] = _load_json(path)
    return result


def _pdf_output_paths(input_path: str, output: str | None, manifest: str | None) -> tuple[Path, Path]:
    source = Path(input_path)
    return (
        Path(output) if output else source.with_suffix(".txt"),
        Path(manifest) if manifest else source.with_suffix(".pages.json"),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="discourse-atlas")
    sub = parser.add_subparsers(dest="command", required=True)

    validate_parser = sub.add_parser("validate", help="Validate an analysis JSON file")
    validate_parser.add_argument("input")

    mermaid_parser = sub.add_parser("mermaid", help="Export a Mermaid flowchart")
    mermaid_parser.add_argument("input")
    mermaid_parser.add_argument("-o", "--output")

    dot_parser = sub.add_parser("dot", help="Export Graphviz DOT")
    dot_parser.add_argument("input")
    dot_parser.add_argument("-o", "--output")

    pdf_parser = sub.add_parser("ingest-pdf", help="Extract PDF text with page and Unicode character coordinates")
    pdf_parser.add_argument("input")
    pdf_parser.add_argument("-o", "--output", help="Output text path; defaults to INPUT.txt")
    pdf_parser.add_argument("--manifest", help="Page manifest JSON path; defaults to INPUT.pages.json")
    pdf_parser.add_argument("--force", action="store_true", help="Overwrite existing output files")

    align_parser = sub.add_parser("align", help="Propose an inspectable source-anchor unit alignment")
    align_parser.add_argument("reference")
    align_parser.add_argument("candidate")
    align_parser.add_argument("--threshold", type=float, default=0.5)
    align_parser.add_argument("-o", "--output")

    evaluate_parser = sub.add_parser("evaluate", help="Evaluate candidate against one reference")
    evaluate_parser.add_argument("reference")
    evaluate_parser.add_argument("candidate")
    evaluate_parser.add_argument("--alignment", help="Explicit split/merge-capable unit alignment JSON")

    multi_parser = sub.add_parser("multi-evaluate", help="Evaluate candidate against multiple defensible references")
    multi_parser.add_argument("candidate")
    multi_parser.add_argument("references", nargs="+")
    multi_parser.add_argument("--auto-align", action="store_true", help="Generate deterministic anchor-overlap proposals per reference")
    multi_parser.add_argument("--threshold", type=float, default=0.5)
    multi_parser.add_argument("--alignment-map", action="append", metavar="REFERENCE=ALIGNMENT_JSON", help="Explicit alignment for one reference; repeat as needed")

    agreement_parser = sub.add_parser("agreement", help="Compare two reconstructions symmetrically")
    agreement_parser.add_argument("left")
    agreement_parser.add_argument("right")
    agreement_parser.add_argument("--alignment", help="Explicit split/merge-capable unit alignment JSON")

    args = parser.parse_args(argv)

    if args.command == "ingest-pdf":
        output_path, manifest_path = _pdf_output_paths(args.input, args.output, args.manifest)
        if output_path.resolve() == manifest_path.resolve():
            print("ERROR: text output and manifest paths must be different", file=sys.stderr)
            return 2
        existing = [path for path in (output_path, manifest_path) if path.exists()]
        if existing and not args.force:
            print(f"ERROR: output already exists: {', '.join(str(path) for path in existing)}; use --force to overwrite", file=sys.stderr)
            return 2
        try:
            source_text, manifest = ingest_pdf(args.input)
        except (PdfDependencyError, ValueError, OSError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(source_text, encoding="utf-8")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {output_path} and {manifest_path}")
        if manifest["empty_page_count"]:
            print(
                f"WARNING: {manifest['empty_page_count']} of {manifest['page_count']} pages yielded no text; OCR is not performed",
                file=sys.stderr,
            )
        return 0

    if args.command == "align":
        pair = _validated_pair(args.reference, args.candidate)
        if pair is None:
            return 1
        try:
            alignment = propose_alignment(*pair, threshold=args.threshold)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        _write_json(alignment, args.output)
        return 0

    if args.command == "evaluate":
        pair = _validated_pair(args.reference, args.candidate)
        if pair is None:
            return 1
        reference, candidate = pair
        if args.alignment:
            alignment = _load_json(args.alignment)
            errors = validate_alignment_document(alignment, reference, candidate)
            if errors:
                for error in errors:
                    print(f"ERROR alignment: {error}", file=sys.stderr)
                return 1
            report = evaluate_with_alignment(reference, candidate, alignment)
        else:
            report = evaluate_documents(reference, candidate)
        _write_json(report)
        return 0

    if args.command == "multi-evaluate":
        candidate = _validated_document(args.candidate, "candidate")
        if candidate is None:
            return 1
        references: list[tuple[str, dict]] = []
        for path in args.references:
            reference = _validated_document(path, f"reference {path}")
            if reference is None:
                return 1
            references.append((path, reference))
        try:
            alignments = _parse_alignment_specs(args.alignment_map)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        if args.auto_align:
            for label, reference in references:
                alignments.setdefault(label, propose_alignment(reference, candidate, args.threshold))
        for label, reference in references:
            if label in alignments:
                errors = validate_alignment_document(alignments[label], reference, candidate)
                if errors:
                    for error in errors:
                        print(f"ERROR alignment {label}: {error}", file=sys.stderr)
                    return 1
        _write_json(evaluate_against_references(references, candidate, alignments))
        return 0

    if args.command == "agreement":
        pair = _validated_pair(args.left, args.right)
        if pair is None:
            return 1
        left, right = pair
        if args.alignment:
            alignment = _load_json(args.alignment)
            errors = validate_alignment_document(alignment, left, right)
            if errors:
                for error in errors:
                    print(f"ERROR alignment: {error}", file=sys.stderr)
                return 1
            report = compare_annotations_with_alignment(left, right, alignment)
        else:
            report = compare_annotations(left, right)
        _write_json(report)
        return 0

    document = _load_json(args.input)
    errors = validate_document(document)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.command == "validate":
        print("valid")
        return 0
    if args.command == "mermaid":
        _write_or_print(to_mermaid(document), args.output)
        return 0
    if args.command == "dot":
        _write_or_print(to_dot(document), args.output)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
