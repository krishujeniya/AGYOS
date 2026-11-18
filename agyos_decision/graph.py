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
STATE_DIR = REPO_ROOT / ".agents" / "state"
GRAPH_FILE = STATE_DIR / "skills-roles-graph.xml"
MANIFEST_FILE = REPO_ROOT / ".agents" / "skills-manifest.json"


def build_skills_roles_graph() -> str:
    """Build the complete enterprise semantic graph and write to .agents/state/skills-roles-graph.xml."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    roles = list_roles()

    skills_data = []
    if MANIFEST_FILE.is_file():
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
    return graph_xml


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
        from .xml_compiler import minify_xml
        return minify_xml(raw_xml)
    return raw_xml
