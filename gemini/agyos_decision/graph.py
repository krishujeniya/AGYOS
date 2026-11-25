"""AGYOS Semantic Graph Engine.

Constructs and queries the enterprise knowledge graph connecting 12 departments,
5 operational pods, 104 corporate roles, and 2,247 physical skills into an
explicit XML Directed Acyclic Graph (DAG).
"""

from __future__ import annotations

import functools
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.sax.saxutils import escape as xml_escape

from .roles import list_roles, get_role, get_skills_for_role, get_all_skills_for_role

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = REPO_ROOT / "state"
GRAPH_FILE_TOON = STATE_DIR / "skills-roles-graph.toon"
GRAPH_FILE = STATE_DIR / "skills-roles-graph.xml"
MANIFEST_FILE_TOON = REPO_ROOT / "skills-manifest.toon"
MANIFEST_FILE = REPO_ROOT / "skills-manifest.json"


def build_skills_roles_graph() -> str:
    """Build the complete enterprise semantic graph and write to state/skills-roles-graph.xml."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    roles = list_roles()

    skills_data = []
    if MANIFEST_FILE_TOON.is_file():
        try:
            from .toon_config import load_toon_manifest
            skills_data = load_toon_manifest(MANIFEST_FILE_TOON)
        except Exception:
            skills_data = []
    elif MANIFEST_FILE.is_file():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                skills_data = json.load(f).get("skills", [])
        except Exception:
            skills_data = []

    departments = sorted({r.department for r in roles})
    pods = sorted({r.governing_pod for r in roles})

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<skills_roles_graph total_departments="{len(departments)}" total_pods="{len(pods)}" total_roles="{len(roles)}" total_skills="{len(skills_data)}">',
        '  <departments>'
    ]
    for d in departments:
        xml_lines.append(f'    <department id="{d}" />')
    xml_lines.append('  </departments>')

    xml_lines.append('  <pods>')
    for p in pods:
        xml_lines.append(f'    <pod id="{p}" />')
    xml_lines.append('  </pods>')

    xml_lines.append('  <roles>')
    for r in roles:
        all_s = get_all_skills_for_role(r.role_id)
        xml_lines.append(
            f'    <role id="{r.role_id}" title="{xml_escape(r.title)}" department="{r.department}" '
            f'pod="{r.governing_pod}" seniority="{r.seniority}" risk="{r.default_risk}" '
            f'mapped_skills="{len(all_s)}" />'
        )
    xml_lines.append('  </roles>')

    xml_lines.append('  <skills>')
    for s in skills_data:
        xml_lines.append(
            f'    <skill id="{s["name"]}" tier="{s.get("tier", 2)}" />'
        )
    xml_lines.append('  </skills>')

    xml_lines.append('  <edges>')
    for r in roles:
        primary_set = set(r.primary_skills)
        all_s = get_all_skills_for_role(r.role_id)
        for s in all_s:
            edge_type = "primary_skill" if s in primary_set else "specialized_skill"
            xml_lines.append(
                f'    <edge from="{r.role_id}" to="{s}" type="{edge_type}" />'
            )
    xml_lines.append('  </edges>')
    xml_lines.append('</skills_roles_graph>')

    graph_xml = "\n".join(xml_lines)
    GRAPH_FILE.write_text(graph_xml, encoding="utf-8")

    # Also emit canonical TOON representation
    toon_lines = [
        f"total_departments: {len(departments)}",
        f"total_pods: {len(pods)}",
        f"total_roles: {len(roles)}",
        f"total_skills: {len(skills_data)}",
        f"departments[{len(departments)}]: {', '.join(departments)}",
        f"pods[{len(pods)}]: {', '.join(pods)}",
        f"roles[{len(roles)}]{{id, title, department, pod, seniority, risk, mapped_skills}}:",
    ]
    for r in roles:
        all_s = get_all_skills_for_role(r.role_id)
        title_json = json.dumps(r.title)
        toon_lines.append(
            f"  - {r.role_id}, {title_json}, {r.department}, {r.governing_pod}, {r.seniority}, {r.default_risk}, {len(all_s)}"
        )
    toon_lines.append(f"skills[{len(skills_data)}]{{id, tier}}:")
    for s in skills_data:
        toon_lines.append(f"  - {s['name']}, {s.get('tier', 2)}")
    toon_lines.append(f"edges[{len(roles) * 10}]{{from, to, type}}:")
    edge_count = 0
    for r in roles:
        primary_set = set(r.primary_skills)
        all_s = get_all_skills_for_role(r.role_id)
        for s in all_s:
            edge_type = "primary_skill" if s in primary_set else "specialized_skill"
            toon_lines.append(f"  - {r.role_id}, {s}, {edge_type}")
            edge_count += 1
    # Patch exact edge count header
    toon_lines[-edge_count - 1] = f"edges[{edge_count}]{{from, to, type}}:"
    GRAPH_FILE_TOON.write_text("\n".join(toon_lines) + "\n", encoding="utf-8")

    return graph_xml


@functools.lru_cache(maxsize=128)
def get_role_subgraph_toon(role_id: str, depth: int = 1) -> str:
    """Extract a lightweight sub-graph for a given role in TOON format."""
    role = get_role(role_id)
    if not role:
        return f"subgraph:\n  role_id: {role_id}\n  status: not_found"

    primary_skills = get_skills_for_role(role_id, all_skills=False)
    lines = [
        "subgraph:",
        f"  role_id: {role.role_id}",
        f"  department: {role.department}",
        f"  pod: {role.governing_pod}",
        f"  seniority: {role.seniority}",
        f"  primary_skills[{len(primary_skills)}]: {', '.join(primary_skills)}",
    ]
    if depth >= 2:
        peers = [r.role_id for r in list_roles() if r.governing_pod == role.governing_pod and r.role_id != role.role_id][:5]
        lines.append(f"  cross_functional_peers[{len(peers)}]: {', '.join(peers)}")
    return "\n".join(lines)


@functools.lru_cache(maxsize=128)
def get_role_subgraph(role_id: str, depth: int = 1, compact: bool = False) -> str:
    """Extract a lightweight 1-hop or 2-hop sub-graph for a given role to inject into prompt context."""
    role = get_role(role_id)
    if not role:
        return f'<subgraph role_id="{role_id}" status="not_found" />'

    primary_skills = get_skills_for_role(role_id, all_skills=False)
    xml_lines = [
        f'<subgraph role_id="{role.role_id}" department="{role.department}" pod="{role.governing_pod}" seniority="{role.seniority}">',
        f'  <primary_skills count="{len(primary_skills)}">'
    ]
    for s in primary_skills:
        xml_lines.append(f'    <skill id="{s}" tier="1" />')
    xml_lines.append('  </primary_skills>')

    if depth >= 2:
        peers = [r.role_id for r in list_roles() if r.governing_pod == role.governing_pod and r.role_id != role.role_id][:5]
        xml_lines.append(f'  <cross_functional_peers count="{len(peers)}">')
        for p in peers:
            xml_lines.append(f'    <peer id="{p}" />')
        xml_lines.append('  </cross_functional_peers>')

    xml_lines.append('</subgraph>')
    raw_xml = "\n".join(xml_lines)
    if compact:
        from .toon_compiler import minify_toon
        return minify_toon(raw_xml)
    return raw_xml
