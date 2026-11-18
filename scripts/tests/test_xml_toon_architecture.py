"""Tests for AGYOS FAANG/MANGO XML & TOON Hybrid Architecture.

Validates:
1. TOON (Token-Oriented Object Notation) encoding and decoding round-trip.
2. Token efficiency reduction (>35% vs JSON on skill catalog datasets).
3. XML compilation of skills, agents, and task contracts with CDATA protection.
4. Parsing validity of all 104 agent XML blocks in .agents/agents/role-*.md.
5. Sampling validity of pre-compiled XML skill cards in .agents/skills-xml/.
6. Parsing validity and structure of .agents/state/skills-roles-graph.xml.
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
from agyos_decision.xml_compiler import (
    prune_conversational_filler,
    minify_xml,
    compile_skill_to_xml,
    compile_agent_to_xml,
    compile_task_to_xml,
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


class TestXmlCompiler(unittest.TestCase):
    def test_prune_conversational_filler(self):
        raw = "Certainly! Here is the implementation:\n\ndef foo():\n    return 42"
        pruned = prune_conversational_filler(raw)
        self.assertNotIn("Certainly", pruned)
        self.assertIn("def foo():", pruned)

    def test_compile_skill_to_xml(self):
        xml_str = compile_skill_to_xml("clean-code")
        self.assertIn('<agyos_skill id="clean-code">', xml_str)
        self.assertIn('<intent>', xml_str)
        self.assertIn('<instructions>', xml_str)

        # Ensure valid XML syntax
        root = ET.fromstring(xml_str)
        self.assertEqual(root.tag, "agyos_skill")
        self.assertEqual(root.attrib.get("id"), "clean-code")

    def test_compile_agent_to_xml(self):
        xml_str = compile_agent_to_xml("role-swe")
        self.assertIn('<agyos_agent id="role-swe"', xml_str)
        self.assertIn('<ownership>', xml_str)
        self.assertIn('<defense_invariants>', xml_str)
        self.assertIn('<skills_workspace format="toon"', xml_str)

        # Ensure valid XML syntax
        root = ET.fromstring(xml_str)
        self.assertEqual(root.tag, "agyos_agent")
        self.assertEqual(root.attrib.get("id"), "role-swe")
        self.assertIsNotNone(root.find("ownership"))
        self.assertIsNotNone(root.find("defense_invariants"))

    def test_task_contract_to_xml(self):
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
        xml_str = contract.to_xml()
        self.assertIn('<agyos_task id="tsk_test_xml_001"', xml_str)
        self.assertIn('<customer_outcome>Build microservice authentication gateway</customer_outcome>', xml_str)
        self.assertIn('<token_budget total="12000"', xml_str)
        self.assertIn('<skills_context format="toon">', xml_str)

        # Ensure valid XML syntax
        root = ET.fromstring(xml_str)
        self.assertEqual(root.tag, "agyos_task")
        self.assertEqual(root.attrib.get("id"), "tsk_test_xml_001")

    def test_minify_xml_token_savings(self):
        raw_xml = compile_agent_to_xml("role-swe", compact=False)
        minified = minify_xml(raw_xml)

        self.assertLess(len(minified), len(raw_xml))
        root = ET.fromstring(minified)
        self.assertEqual(root.tag, "agyos_agent")
        self.assertEqual(root.attrib.get("id"), "role-swe")

        cdata_text = root.find("skills_workspace").text.strip()
        decoded = decode_toon(cdata_text)
        self.assertGreater(len(decoded), 0)

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
        cached = compile_cached_prompt(contract, compact=True)
        self.assertIn("static_prefix", cached)
        self.assertIn("dynamic_suffix", cached)
        self.assertIn("full_prompt", cached)

        self.assertIn("<agyos_agent", cached["static_prefix"])
        self.assertIn("<defense_invariants>", cached["static_prefix"])
        self.assertIn("<agyos_task", cached["dynamic_suffix"])
        self.assertIn("Build caching proxy gateway", cached["dynamic_suffix"])

        agent_elem = ET.fromstring(cached["static_prefix"])
        task_elem = ET.fromstring(cached["dynamic_suffix"])
        self.assertEqual(agent_elem.tag, "agyos_agent")
        self.assertEqual(task_elem.tag, "agyos_task")


class TestPrecompiledArtifacts(unittest.TestCase):
    def test_skills_xml_symlink_exists(self):
        symlink = ROOT / "skills-xml"
        self.assertTrue(symlink.exists(), "Root symlink skills-xml does not exist")
        self.assertTrue(symlink.is_symlink() or symlink.is_dir())

    def test_skills_xml_catalog_populated(self):
        xml_dir = ROOT / ".agents" / "skills-xml"
        self.assertTrue(xml_dir.is_dir(), ".agents/skills-xml directory does not exist")
        xml_files = list(xml_dir.glob("*.xml"))
        self.assertGreaterEqual(len(xml_files), 2000, f"Expected >= 2000 XML skill cards, found {len(xml_files)}")

    def test_skills_xml_parse_samples(self):
        xml_dir = ROOT / ".agents" / "skills-xml"
        xml_files = list(xml_dir.glob("*.xml"))[:50]
        for f in xml_files:
            content = f.read_text(encoding="utf-8")
            try:
                root = ET.fromstring(content)
                self.assertEqual(root.tag, "agyos_skill")
            except Exception as e:
                self.fail(f"Failed to parse XML in {f.name}: {e}")

    def test_all_104_agents_have_valid_xml_blocks(self):
        agents_dir = ROOT / ".agents" / "agents"
        role_files = list(agents_dir.glob("role-*.md"))
        self.assertEqual(len(role_files), 104, f"Expected 104 role files, found {len(role_files)}")

        for af in role_files:
            content = af.read_text(encoding="utf-8")
            match = re.search(r"(<agyos_agent[\s\S]*?</agyos_agent>)", content)
            self.assertTrue(match, f"Missing <agyos_agent> XML block in {af.name}")
            xml_block = match.group(1)
            try:
                root = ET.fromstring(xml_block)
                self.assertEqual(root.tag, "agyos_agent")
            except Exception as e:
                self.fail(f"Invalid XML syntax in {af.name}: {e}")

    def test_skills_roles_graph_validity(self):
        graph_file = ROOT / ".agents" / "state" / "skills-roles-graph.xml"
        self.assertTrue(graph_file.exists(), ".agents/state/skills-roles-graph.xml does not exist")

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
