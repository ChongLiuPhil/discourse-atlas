from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = "1.1.0"
PROTOCOL_VERSION = "1.1.0"
CURRENT_GRAPH_SCHEMA = "0.2.0"
LEGACY_GRAPH_SCHEMA = "0.1.0"
ALIGNMENT_SCHEMA = "0.1.0"

GRAPH_FIXTURES = [
    "examples/mini-essay/analysis.json",
    "skills/discourse-structure/examples/mini-essay.analysis.json",
    "benchmark/annotations/mini-essay-a.json",
    "benchmark/annotations/mini-essay-b.json",
    "benchmark/cases/academic-mechanism/gold.json",
    "benchmark/cases/mill-on-liberty/reference-a.json",
    "benchmark/cases/mill-on-liberty/reference-b.json",
    "benchmark/cases/mini-essay/gold.json",
    "benchmark/cases/philosophy-counterexample/gold.json",
    "benchmark/cases/policy-library/gold.json",
]

REQUIRED_PATHS = [
    "START_HERE.md", "START_HERE.zh-CN.md", "AGENT.md", "AGENTS.md", "AGENTS.zh-CN.md",
    "PROJECT_MANIFEST.yaml", "PROJECT_STATUS.md", "ROADMAP.md", "GOVERNANCE.md", "CITATION.cff",
    "docs/versioning.md", "docs/compatibility.md", "docs/release-process.md",
    "docs/decisions/0001-canonical-json.md", "docs/decisions/0002-hierarchy-dependency-separation.md",
    "docs/decisions/0003-relation-ontology.md", "docs/decisions/0004-schema-versioning.md",
    "schemas/discourse-graph/0.2.0.schema.json", "schemas/discourse-graph/0.1.0-legacy.schema.json",
    "schemas/node-alignment/0.1.0.schema.json",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"repository consistency error: {message}")


for path in REQUIRED_PATHS:
    require((ROOT / path).exists(), f"missing required path: {path}")

require(f'version = "{RELEASE_VERSION}"' in read("pyproject.toml"), "pyproject release version")
require(f'__version__ = "{RELEASE_VERSION}"' in read("src/discourse_atlas/__init__.py"), "Python package version")
require(json.loads(read("apps/web/package.json"))["version"] == RELEASE_VERSION, "web package version")
require(f'version: "{RELEASE_VERSION}"' in read("CITATION.cff"), "citation version")
require(f'release_version: "{RELEASE_VERSION}"' in read("PROJECT_MANIFEST.yaml"), "manifest release version")
require(f"Protocol version: **{PROTOCOL_VERSION}**" in read("AGENT.md"), "Agent protocol version")
require(f'remote_agent_protocol: "{PROTOCOL_VERSION}"' in read("PROJECT_MANIFEST.yaml"), "manifest protocol version")

current_alias = json.loads(read("schemas/discourse-graph.schema.json"))
current_versioned = json.loads(read("schemas/discourse-graph/0.2.0.schema.json"))
current_packaged = json.loads(read("src/discourse_atlas/resources/discourse-graph.schema.json"))
require(current_alias == current_versioned == current_packaged, "current graph schema copies differ")
require(current_alias["properties"]["schema_version"]["const"] == CURRENT_GRAPH_SCHEMA, "current graph schema version")

legacy_repo = json.loads(read("schemas/discourse-graph/0.1.0-legacy.schema.json"))
legacy_packaged = json.loads(read("src/discourse_atlas/resources/discourse-graph-0.1.0-legacy.schema.json"))
require(legacy_repo == legacy_packaged, "legacy graph schema copies differ")
require(legacy_repo["properties"]["schema_version"]["const"] == LEGACY_GRAPH_SCHEMA, "legacy graph schema version")

alignment = json.loads(read("schemas/node-alignment.schema.json"))
alignment_versioned = json.loads(read("schemas/node-alignment/0.1.0.schema.json"))
require(alignment["properties"]["alignment_version"]["const"] == ALIGNMENT_SCHEMA, "alignment schema version")
require(alignment_versioned["properties"]["alignment_version"]["const"] == ALIGNMENT_SCHEMA, "versioned alignment schema version")

for path in GRAPH_FIXTURES:
    document = json.loads(read(path))
    require(document.get("schema_version") == CURRENT_GRAPH_SCHEMA, f"{path} is not on current graph schema")

for path in ("README.md", "README.zh-CN.md"):
    text = read(path)
    require("v1.1.0" in text, f"{path} release status")
    require("0.2.0" in text, f"{path} current schema status")

require("Future interactive viewer" not in read("docs/architecture.md"), "architecture still calls viewer future")
require("AGENT.md" in read("START_HERE.md") and "AGENTS.md" in read("START_HERE.md"), "English onboarding role distinction")
require("AGENT.md" in read("START_HERE.zh-CN.md") and "AGENTS.md" in read("START_HERE.zh-CN.md"), "Chinese onboarding role distinction")

print("repository consistency: OK")
