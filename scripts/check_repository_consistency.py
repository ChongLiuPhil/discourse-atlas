from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "PROJECT_MANIFEST.yaml"
CONTEXT_INTERFACE_PATH = ROOT / "PROJECT_CONTEXT_INTERFACE.yaml"


def read(path: str | Path) -> str:
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    return path.read_text(encoding="utf-8")


def load_yaml(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(read(path))
    if not isinstance(data, dict):
        raise SystemExit(f"repository consistency error: expected mapping in {path}")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"repository consistency error: {message}")


def resolve_ref(manifest: dict[str, Any], dotted_ref: str) -> Any:
    current: Any = manifest
    for part in dotted_ref.split('.'):
        require(isinstance(current, dict) and part in current, f'unresolved manifest ref: {dotted_ref}')
        current = current[part]
    return current


def is_repository_path(value: str) -> bool:
    if value.startswith(('http://', 'https://')):
        return False
    suffixes = ('.md', '.json', '.py', '.yaml', '.yml', '.cff', '.toml', '.jsx', '.js')
    return '/' in value or value.endswith(suffixes)


def iter_resource_paths(node: Any):
    if isinstance(node, dict):
        for value in node.values():
            yield from iter_resource_paths(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_resource_paths(value)
    elif isinstance(node, str) and is_repository_path(node):
        yield node


def heading_signature(text: str) -> list[int]:
    return [len(match.group(1)) for line in text.splitlines() if (match := re.match(r'^(#{1,6})\s+', line))]


def normalized_local_links(text: str) -> set[str]:
    targets = set()
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if target.startswith(('http://', 'https://', '#')):
            continue
        targets.add(target.replace('.zh-CN.md', '.md'))
    return targets


def external_urls(text: str) -> set[str]:
    return set(re.findall(r'https://[^\s)>`]+', text))


manifest = load_yaml(MANIFEST_PATH)
context = load_yaml(CONTEXT_INTERFACE_PATH)['project_context_interface']
ahicp_manifest = load_yaml('AHICP_MANIFEST.yaml')
stack = load_yaml('project-stack.yaml')
stack_lock = load_yaml('project-stack.lock.yaml')
publishing = load_yaml('publishing.yaml')
website = load_yaml('website.yaml')

release_version = manifest['project']['release_version']
protocol_version = manifest['versions']['remote_agent_protocol']
graph = manifest['versions']['discourse_graph_schema']
alignment = manifest['versions']['node_alignment_schema']
current_graph_schema = graph['current']
legacy_graph_schema = '0.1.0'
alignment_schema = alignment['current']

# Manifest-declared repository resources must exist.
for section_name in ('entry_points', 'collaboration', 'canonical', 'implementation', 'applications', 'quality'):
    for resource_path in iter_resource_paths(manifest[section_name]):
        require((ROOT / resource_path).exists(), f'manifest target does not exist: {resource_path}')

# Context interface routes must resolve exclusively through Manifest references.
require(context['control_plane']['manifest'] == MANIFEST_PATH.name, 'context interface points to unexpected manifest')
routes = context['task_routes']
expected_routes = {'SEMANTICS', 'SCHEMA', 'IMPLEMENTATION', 'WEB', 'BENCHMARK', 'DOCS', 'RELEASE', 'GOVERNANCE'}
require(set(routes) == expected_routes, 'context interface task routes differ from repository change classes')
for route_name, route in routes.items():
    for key in ('required_refs', 'optional_refs'):
        for dotted_ref in route.get(key, []):
            resolved = resolve_ref(manifest, dotted_ref)
            require(isinstance(resolved, str), f'{route_name} ref is not a string path: {dotted_ref}')
            require(is_repository_path(resolved), f'{route_name} ref is not a repository path: {dotted_ref}')
            require((ROOT / resolved).exists(), f'{route_name} ref target missing: {dotted_ref} -> {resolved}')

# Release/protocol versions are derived from the Manifest, not duplicated here.
pyproject = read('pyproject.toml')
match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
require(match is not None and match.group(1) == release_version, 'pyproject release version')

init_text = read('src/discourse_atlas/__init__.py')
match = re.search(r'__version__\s*=\s*"([^"]+)"', init_text)
require(match is not None and match.group(1) == release_version, 'Python package version')

web_package = json.loads(read('apps/web/package.json'))
web_lock = json.loads(read('apps/web/package-lock.json'))
require(web_package['version'] == release_version, 'web package version')
require(web_lock['version'] == release_version, 'web lockfile version')
require(web_lock['packages']['']['version'] == release_version, 'web lockfile root package version')

citation = load_yaml('CITATION.cff')
require(str(citation['version']) == release_version, 'citation version')

agent_text = read(manifest['entry_points']['remote_analysis_protocol'])
require(f'Protocol version: **{protocol_version}**' in agent_text, 'remote Agent protocol version')

# Versioned and packaged schemas must agree with Manifest-declared versions.
current_alias = json.loads(read(graph['latest_alias']))
current_versioned = json.loads(read(graph['versioned']))
current_packaged = json.loads(read('src/discourse_atlas/resources/discourse-graph.schema.json'))
require(current_alias == current_versioned == current_packaged, 'current graph schema copies differ')
require(current_alias['properties']['schema_version']['const'] == current_graph_schema, 'current graph schema version')

legacy_repo = json.loads(read(graph['legacy_0_1_profile']))
legacy_packaged = json.loads(read('src/discourse_atlas/resources/discourse-graph-0.1.0-legacy.schema.json'))
require(legacy_repo == legacy_packaged, 'legacy graph schema copies differ')
require(legacy_repo['properties']['schema_version']['const'] == legacy_graph_schema, 'legacy graph schema version')

alignment_alias = json.loads(read(alignment['latest_alias']))
alignment_versioned = json.loads(read(alignment['versioned']))
alignment_alias_contract = {key: value for key, value in alignment_alias.items() if key != '$id'}
alignment_versioned_contract = {key: value for key, value in alignment_versioned.items() if key != '$id'}
require(alignment_alias_contract == alignment_versioned_contract, 'alignment schema contracts differ beyond $id')
require(alignment_alias['properties']['alignment_version']['const'] == alignment_schema, 'alignment schema version')

# All maintained graph fixtures should use the current graph schema.
graph_fixtures = [
    'examples/mini-essay/analysis.json',
    'skills/discourse-structure/examples/mini-essay.analysis.json',
    'benchmark/annotations/mini-essay-a.json',
    'benchmark/annotations/mini-essay-b.json',
    'benchmark/cases/academic-mechanism/gold.json',
    'benchmark/cases/mill-on-liberty/reference-a.json',
    'benchmark/cases/mill-on-liberty/reference-b.json',
    'benchmark/cases/mini-essay/gold.json',
    'benchmark/cases/philosophy-counterexample/gold.json',
    'benchmark/cases/policy-library/gold.json',
]
for fixture_path in graph_fixtures:
    document = json.loads(read(fixture_path))
    require(document.get('schema_version') == current_graph_schema, f'{fixture_path} is not on current graph schema')

# Bilingual entry pairs: existence is manifest-driven; structure and links must stay aligned.
for entry_name, entry in manifest['entry_points'].items():
    if not isinstance(entry, dict) or 'canonical' not in entry or 'mirror' not in entry:
        continue
    canonical_text = read(entry['canonical'])
    mirror_text = read(entry['mirror'])
    require(heading_signature(canonical_text) == heading_signature(mirror_text), f'{entry_name} heading structure differs across languages')
    require(normalized_local_links(canonical_text) == normalized_local_links(mirror_text), f'{entry_name} local links differ across languages')
    require(external_urls(canonical_text) == external_urls(mirror_text), f'{entry_name} external URLs differ across languages')

readme_pair = manifest['entry_points']['human_readme']
for path in (readme_pair['canonical'], readme_pair['mirror']):
    text = read(path)
    require(f'v{release_version}' in text, f'{path} release status')
    require(current_graph_schema in text, f'{path} current schema status')

# Route names and operational-resume fields must be visible to humans/agents.
for path in (manifest['entry_points']['repository_onboarding']['canonical'], manifest['entry_points']['repository_onboarding']['mirror']):
    text = read(path)
    for route_name in expected_routes:
        require(route_name in text, f'{path} missing route {route_name}')
    require('PROJECT_CONTEXT_INTERFACE.yaml' in text, f'{path} missing context interface')

status_text = read(manifest['canonical']['project_status'])
for heading in ('### Current objective', '### Immediate next action', '### Active work', '### Blockers', '### Pending maintainer decisions', '### Synchronization defects'):
    require(heading in status_text, f'project status missing operational field: {heading}')

pr_template = read('.github/pull_request_template.md')
require('## Decision authority' in pr_template, 'PR template missing decision authority')
require('AI-PROPOSED' in pr_template, 'PR template missing AI proposal state')

require('Future interactive viewer' not in read('docs/architecture.md'), 'architecture still calls viewer future')
require('npm ci --no-audit --no-fund' in read('.github/workflows/ci.yml'), 'CI does not use npm ci')
require('npm ci --no-audit --no-fund' in read('.github/workflows/pages.yml'), 'Pages does not use npm ci')

# Inquiry Publishing Stack v2: stable composition/template revisions remain
# distinct from the newer semantic framework revisions adopted by this project.
require(stack.get('schema') == 'inquiry-publishing-stack/v2', 'project stack schema')
require(stack_lock.get('schema') == 'inquiry-publishing-stack-lock/v2', 'project stack lock schema')
require(stack.get('project', {}).get('id') == 'discourse-atlas', 'project stack id')
require(stack.get('profile') == 'full-research-publication', 'project stack composition profile')

template_pins = {
    'AHICP': '02d0b3c02ca23073c760b6e0f761a468e0235a1c',
    'PPF': '9a6005de85f032095e36eea03fda317e73126538',
    'Vault': '592c6e2e938f995b7b3e7df07a72f7f1e2c50c5a',
    'Starter': '05857086e240cbd269eae91af8419ea0921c01fa',
}
adopted_pins = {
    'AHICP': 'ed5a60b1016497472072db108072ace59bcdb65d',
    'PPF': 'e660b48fb216c28c8faa1f0fe2d0816401e1de2c',
    'Vault': '79d64b12275a5cc7c09236b144bf4213fa7afc5e',
}

components = stack['components']
require(components['governance']['template_source_commit'] == template_pins['AHICP'], 'AHICP template pin')
require(components['governance']['project_adopted_commit'] == adopted_pins['AHICP'], 'AHICP adopted pin')
require(components['publishing']['template_source_commit'] == template_pins['PPF'], 'PPF template pin')
require(components['publishing']['project_adopted_commit'] == adopted_pins['PPF'], 'PPF adopted pin')
require(components['portfolio_interface']['template_source_commit'] == template_pins['Vault'], 'Vault template pin')
require(components['portfolio_interface']['project_adopted_commit'] == adopted_pins['Vault'], 'Vault adopted pin')
require(stack['starter']['adopted_commit'] == template_pins['Starter'], 'Starter source revision')
require(stack_lock['resolved'] == {
    'ahicp': template_pins['AHICP'],
    'ppf': template_pins['PPF'],
    'vault_interface': template_pins['Vault'],
    'starter': template_pins['Starter'],
}, 'Stack lock does not match stable composition revisions')

ahicp = ahicp_manifest['ahicp']
require(ahicp['template_source_commit'] == template_pins['AHICP'], 'AHICP manifest template pin')
require(ahicp['adopted_protocol_commit'] == adopted_pins['AHICP'], 'AHICP manifest adopted pin')
require(ahicp['compatibility']['project_native_manifest'] == 'PROJECT_MANIFEST.yaml', 'AHICP adapter native manifest')
require(ahicp['compatibility']['project_native_context_interface'] == 'PROJECT_CONTEXT_INTERFACE.yaml', 'AHICP adapter native context interface')

web = publishing['publication']['web']
deployment = publishing['deployment']['web']
require(web['enabled'] is True, 'Hosted Atlas publication must remain enabled')
require(web['authorization_state'] == 'authorized', 'Hosted Atlas public authorization drift')
require(web['visibility'] == 'public', 'Hosted Atlas visibility drift')
require(deployment['provider'] == 'github-pages', 'Hosted Atlas provider drift')
require(deployment['integration_state'] == 'PRODUCTION_ACTIVE', 'Hosted Atlas integration state drift')
require(deployment['production_url'] == 'https://chongliuphil.github.io/discourse-atlas/', 'Hosted Atlas production URL drift')
require(deployment['auto_deploy_on_main'] is True, 'Hosted Atlas main auto-deploy drift')
require(deployment['endpoint_verification'] is True, 'Hosted Atlas endpoint verification drift')
require(publishing['release']['require_explicit_release'] is True, 'toolkit release must remain explicit')
require(publishing['release']['continuous_web_is_release'] is False, 'Pages deployment must remain distinct from toolkit release semantics')

require(website.get('publish') is False, 'Academic Vault/homepage publication boundary must remain publish=false')
website_notes = str(website.get('publication_notes', ''))
require('does not revoke' in website_notes, 'website metadata must preserve existing Hosted Atlas publication nuance')

pages = read('.github/workflows/pages.yml')
require('actions/deploy-pages@v4' in pages, 'Pages deployment action drift')
require('https://chongliuphil.github.io/discourse-atlas/' in pages, 'Pages verification URL drift')
require((ROOT / 'docs/decisions/0006-inquiry-publishing-stack-adapter.md').exists(), 'Decision 0006 missing')
require('0006-inquiry-publishing-stack-adapter.md' in read('docs/decisions/README.md'), 'Decision 0006 not indexed')

print('repository consistency: OK')
