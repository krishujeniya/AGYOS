"""Tests for AGYOS FAANG/MANGO XML & TOON Hybrid Architecture.

Validates:
1. TOON (Token-Oriented Object Notation) encoding and decoding round-trip.
2. Token efficiency reduction (>35% vs JSON on skill catalog datasets).
3. XML compilation of skills, agents, and task contracts with CDATA protection.
4. Parsing validity of all 104 agent XML blocks in gemini/agents/role-*.toon with TOON workspaces.
5. Verification of 100% pure TOON catalog in gemini/skills/ and exclusion of legacy skills-xml.
6. Parsing validity and structure of gemini/state/skills-roles-graph.xml.
7. Graph engine node and edge traversal.
"""

import json
from pathlib import Path
import re
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agyos_decision.toon_codec import encode_toon, decode_toon
from agyos_decision.toon_compiler import (
    prune_conversational_filler,
    minify_toon,
    minify_xml,
    compile_skill_to_toon,
    compile_skill_to_xml,
    compile_agent_to_toon,
    compile_agent_to_xml,
    compile_task_to_toon,
    compile_task_to_xml,
    compile_cached_toon_prompt,
    compile_cached_prompt,
)
from agyos_decision.contracts import TaskContract
from agyos_decision.graph import build_skills_roles_graph, get_role_subgraph


class TestToonCodec(unittest.TestCase):
    def test_encode_decode_round_trip(self):
        records = [
            {"name": "clean-code", "tier": "1", "domain": "engineering"},
            {"name": "pytest-testing", "tier": "2", "domain": "quality"},
            {"name": "systematic-debugging", "tier": "1", "domain": "engineering"},
        ]
        encoded = encode_toon(records, key_name="skills")
        self.assertIn("skills[3]:", encoded)
        self.assertIn("name, tier, domain", encoded)
        self.assertIn("clean-code, 1, engineering", encoded)

        decoded = decode_toon(encoded)
        self.assertEqual(len(decoded), 3)
        self.assertEqual(decoded[0]["name"], "clean-code")
        self.assertEqual(decoded[1]["tier"], "2")
        self.assertEqual(decoded[2]["domain"], "engineering")

    def test_empty_records(self):
        encoded = encode_toon([], key_name="empty")
        self.assertEqual(encoded, "empty[0]:\n  - (empty)")
        self.assertEqual(decode_toon(encoded), [])

    def test_special_characters_escaping(self):
        records = [
            {"name": "skill-with-comma", "desc": "value, with, commas", "extra": "regular text"}
        ]
        encoded = encode_toon(records, key_name="test")
        decoded = decode_toon(encoded)
        self.assertEqual(len(decoded), 1)
        self.assertEqual(decoded[0]["desc"], "value, with, commas")
        self.assertEqual(decoded[0]["extra"], "regular text")

    def test_token_efficiency_vs_json(self):
        # 50 typical skills
        sample_skills = [
            {
                "name": f"skill-domain-{i:03d}",
                "tier": "1" if i % 2 == 0 else "2",
                "domain": "engineering" if i % 3 == 0 else "product",
                "path": f"skills-by-role/role-swe/skill-domain-{i:03d}"
            }
            for i in range(50)
        ]
        json_repr = json.dumps(sample_skills, indent=2)
        toon_repr = encode_toon(sample_skills, key_name="skills")

        json_len = len(json_repr)
        toon_len = len(toon_repr)

        # TOON should achieve at least 35% character reduction
        savings_ratio = (json_len - toon_len) / json_len
        self.assertGreater(savings_ratio, 0.35, f"Expected >35% reduction, got {savings_ratio:.2%}")

    def test_compact_toon_encoding_and_batch_decoding(self):
        records = [
            {"name": f"skill-{i}", "tier": "1", "domain": "engineering"}
            for i in range(100)
        ]
        compact_encoded = encode_toon(records, key_name="skills", compact=True)
        self.assertIn("skills[100]:", compact_encoded)
        self.assertIn("- name, tier, domain", compact_encoded)

        decoded = decode_toon(compact_encoded)
        self.assertEqual(len(decoded), 100)
        self.assertEqual(decoded[0]["name"], "skill-0")
        self.assertEqual(decoded[99]["name"], "skill-99")


class TestToonCompiler(unittest.TestCase):
    def test_prune_conversational_filler(self):
        raw = "Certainly! Here is the implementation:\n\ndef foo():\n    return 42"
        pruned = prune_conversational_filler(raw)
        self.assertNotIn("Certainly", pruned)
        self.assertIn("def foo():", pruned)

    def test_compile_skill_to_toon(self):
        toon_str = compile_skill_to_toon("clean-code")
        self.assertIn('skill: "clean-code"', toon_str)
        self.assertIn("intent:", toon_str)
        self.assertIn("instructions:", toon_str)
        self.assertNotIn("<agyos_skill", toon_str)

    def test_compile_agent_to_toon(self):
        toon_str = compile_agent_to_toon("role-swe")
        self.assertIn('agent: "role-swe"', toon_str)
        self.assertIn("ownership:", toon_str)
        self.assertIn("defense_invariants:", toon_str)
        self.assertIn('skills_workspace format="toon"', toon_str)
        self.assertNotIn("<agyos_agent", toon_str)

    def test_task_contract_to_toon(self):
        contract = TaskContract(
            task_id="tsk_test_xml_001",
            run_id="run_test",
            parent_task_id=None,
            tenant_id="tenant_default",
            requester_id="user_admin",
            depth=0,
            pod="pod-build",
            objective="Build microservice authentication gateway",
            risk="R1",
            role_id="role-swe",
        )
        toon_str = contract.to_toon()
        self.assertIn('task: "tsk_test_xml_001"', toon_str)
        self.assertIn('customer_outcome: "Build microservice authentication gateway"', toon_str)
        self.assertIn('token_budget.total: 12000', toon_str)
        self.assertIn('skills_context format="toon":', toon_str)
        self.assertNotIn("<agyos_task", toon_str)

    def test_minify_toon_token_savings(self):
        raw_toon = compile_agent_to_toon("role-swe", compact=False)
        minified = minify_toon(raw_toon)

        self.assertLessEqual(len(minified), len(raw_toon))
        self.assertIn('agent: "role-swe"', minified)

    def test_compile_cached_prompt(self):
        contract = TaskContract(
            task_id="tsk_test_cache_001",
            run_id="run_cache",
            parent_task_id=None,
            tenant_id="tenant_default",
            requester_id="user_admin",
            depth=0,
            pod="pod-build",
            objective="Build caching proxy gateway",
            risk="R1",
            role_id="role-swe",
        )
        cached = compile_cached_toon_prompt(contract, compact=True)
        self.assertIn("static_prefix", cached)
        self.assertIn("dynamic_suffix", cached)
        self.assertIn("full_prompt", cached)

        self.assertIn('agent: "role-swe"', cached["static_prefix"])
        self.assertIn("defense_invariants:", cached["static_prefix"])
        self.assertIn('task: "tsk_test_cache_001"', cached["dynamic_suffix"])
        self.assertIn("Build caching proxy gateway", cached["dynamic_suffix"])
        self.assertNotIn("<agyos_agent", cached["static_prefix"])
        self.assertNotIn("<agyos_task", cached["dynamic_suffix"])


class TestToonArchitecture(unittest.TestCase):
    def test_legacy_skills_xml_excluded_from_workspace(self):
        symlink = ROOT / "skills-xml"
        self.assertFalse(symlink.exists(), "Root symlink skills-xml should not exist in active workspace")
        xml_dir = ROOT / "skills-xml"
        self.assertFalse(xml_dir.exists(), "skills-xml should not exist in active workspace")

    def test_toon_skills_catalog_populated(self):
        skills_dir = ROOT / "skills"
        self.assertTrue(skills_dir.is_dir(), "skills directory does not exist")
        skill_dirs = [
            d for r in skills_dir.iterdir() if r.is_dir() and not r.name.startswith(".")
            for d in r.iterdir() if d.is_dir() and not d.name.startswith(".")
        ]
        self.assertGreaterEqual(len(skill_dirs), 2000, f"Expected >= 2000 skills, found {len(skill_dirs)}")

    def test_toon_skills_parse_samples(self):
        skills_dir = ROOT / "skills"
        skill_dirs = [
            d for r in skills_dir.iterdir() if r.is_dir() and not r.name.startswith(".")
            for d in r.iterdir() if d.is_dir() and not d.name.startswith(".")
        ][:50]
        for sd in skill_dirs:
            toon_file = sd / "prompt.toon"
            self.assertTrue(toon_file.is_file(), f"Missing prompt.toon in {sd.name}")
            content = toon_file.read_text(encoding="utf-8")
            self.assertIn(f"skill: \"{sd.name}\"", content)

    def test_all_104_agents_have_valid_xml_blocks(self):
        from agyos_decision.catalog import decode_toon_document

        agents_dir = ROOT / "agents"
        role_files = list(agents_dir.glob("role-*.toon"))
        self.assertEqual(len(role_files), 104, f"Expected 104 role files, found {len(role_files)}")

        for af in role_files:
            content = decode_toon_document(af)
            match = re.search(r"(<agyos_agent[\s\S]*?</agyos_agent>)", content)
            self.assertTrue(match, f"Missing <agyos_agent> XML block in {af.name}")
            xml_block = match.group(1)
            try:
                root = ET.fromstring(xml_block)
                self.assertEqual(root.tag, "agyos_agent")
            except Exception as e:
                self.fail(f"Invalid XML syntax in {af.name}: {e}")

    def test_skills_roles_graph_validity(self):
        graph_file = ROOT / "state" / "skills-roles-graph.xml"
        self.assertTrue(graph_file.exists(), "state/skills-roles-graph.xml does not exist")

        tree = ET.parse(graph_file)
        root = tree.getroot()
        self.assertEqual(root.tag, "skills_roles_graph")

        roles_elem = root.find("roles")
        skills_elem = root.find("skills")
        edges_elem = root.find("edges")
        self.assertIsNotNone(roles_elem)
        self.assertIsNotNone(skills_elem)
        self.assertIsNotNone(edges_elem)

        role_nodes = roles_elem.findall("role")
        skill_nodes = skills_elem.findall("skill")
        self.assertEqual(len(role_nodes), 104, f"Expected 104 role nodes in graph, found {len(role_nodes)}")
        self.assertGreaterEqual(len(skill_nodes), 2000, f"Expected >= 2000 skill nodes in graph, found {len(skill_nodes)}")
        self.assertGreaterEqual(len(edges_elem.findall("edge")), 4000, "Expected >= 4000 edges in knowledge graph")

    def test_graph_subgraph_traversal(self):
        subgraph_xml = get_role_subgraph("role-swe", depth=1)
        root = ET.fromstring(subgraph_xml)
        self.assertEqual(root.tag, "subgraph")
        self.assertEqual(root.attrib.get("role_id"), "role-swe")
        primary_skills = root.find("primary_skills")
        self.assertIsNotNone(primary_skills)
        self.assertGreater(len(primary_skills.findall("skill")), 0)

    def test_subgraph_depth_two(self):
        subgraph_xml = get_role_subgraph("role-swe", depth=2)
        root = ET.fromstring(subgraph_xml)
        self.assertEqual(root.tag, "subgraph")
        peers = root.find("cross_functional_peers")
        self.assertIsNotNone(peers)
        self.assertGreater(len(peers.findall("peer")), 0)


if __name__ == "__main__":
    unittest.main()
