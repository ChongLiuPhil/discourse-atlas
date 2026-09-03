from __future__ import annotations

import argparse
import json
import sys
from importlib import resources
from pathlib import Path

from jsonschema import Draft202012Validator

from .validation import validate_references


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _schema() -> dict:
    # Prefer the repository copy during development so schema edits are picked up
    # immediately; fall back to the packaged resource for normal installations.
    repo_schema = _repo_root() / "schemas" / "discourse-graph.schema.json"
    if repo_schema.exists():
        return _load_json(repo_schema)

    packaged = resources.files("discourse_atlas.resources").joinpath(
        "discourse-graph.schema.json"
    )
    with packaged.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_document(document: dict) -> list[str]:
    validator = Draft202012Validator(_schema())
    schema_errors = sorted(validator.iter_errors(document), key=lambda e: list(e.path))
    errors = [
        f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}"
        for e in schema_errors
    ]
    # Semantic validation assumes the basic arrays/objects have schema-valid shapes.
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
        "requires": "requires",
        "supports": "supports",
        "derives": "derives",
        "refines": "refines",
        "contrasts": "contrasts",
        "objects_to": "objects to",
        "responds_to": "responds to",
        "illustrates": "illustrates",
        "sequence": "sequence",
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


def _write_or_print(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


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

    args = parser.parse_args(argv)
    document = _load_json(Path(args.input))
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
