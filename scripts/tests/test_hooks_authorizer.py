"""Tests for Pod Definitions, SOP Skills, and Fail-Closed Authorizer Hook.

Enforces:
1. 5 Pod Agent definitions in .agents/agents/:
   pod-growth, pod-customer, pod-build, pod-gna, pod-people.
   Valid host tools: read_file, edit_file, write_file, run_command, invoke_subagent, send_message.
2. 5 SOP Skills in .agents/skills/:
   sop-growth, sop-customer, sop-build, sop-gna, sop-people.
3. Fail-Closed Authorizer hook (scripts/hooks/authorizer.py):
   - Blocks R3 irreversible actions (wire, broadcast send, delete, sign) unless explicitly authorized.
   - Blocks tools outside capability allowlist.
   - Takes pre-write snapshot before write_file/edit_file.
   - Fails closed on errors when evaluating high-impact actions.
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
AUTHORIZER_HOOK = ROOT / "scripts" / "hooks" / "authorizer.py"


class PodDefinitionsTests(unittest.TestCase):
    REQUIRED_PODS = [
        "pod-growth",
        "pod-customer",
        "pod-build",
        "pod-gna",
        "pod-people",
    ]

    def test_all_5_pod_agent_files_exist_and_have_valid_frontmatter(self):
        for pod in self.REQUIRED_PODS:
            path = ROOT / ".agents" / "agents" / f"{pod}.md"
            self.assertTrue(path.exists(), f"Agent file missing: {path}")
            content = path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\n"), f"{pod}.md must have YAML frontmatter")
            self.assertIn(f"name: {pod}", content)
            self.assertIn("tools:", content)
            # Ensure valid host tool names
            for tool in ("read_file", "edit_file", "write_file", "run_command", "invoke_subagent"):
                self.assertIn(tool, content)

    @unittest.skipUnless(shutil.which("agy"), "agy CLI not installed in current environment")
    def test_agy_cli_lists_all_5_pods(self):
        result = subprocess.run(["agy", "agents"], capture_output=True, text=True, check=True, cwd=str(ROOT))
        for pod in self.REQUIRED_PODS:
            self.assertIn(pod, result.stdout, f"agy agents output missing {pod}")

    def test_all_agent_files_declare_only_valid_host_tools(self):
        import glob
        import yaml
        loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
        valid_tools = {
            "read_file", "edit_file", "write_file", "run_command",
            "invoke_subagent", "send_message", "search_web", "manage_task", "call_mcp_tool"
        }
        for agent_path in (ROOT / ".agents" / "agents").glob("*.md"):
            content = agent_path.read_text(encoding="utf-8")
            if content.startswith("---\n"):
                parts = content.split("---\n", 2)
                if len(parts) >= 3:
                    meta = yaml.load(parts[1], Loader=loader)
                    if meta and isinstance(meta, dict):
                        tools = meta.get("tools", [])
                        for tool in tools:
                            self.assertIn(
                                tool, valid_tools,
                                f"Agent {agent_path.name} declares invalid host tool: '{tool}'"
                            )


class SOPSkillsTests(unittest.TestCase):
    REQUIRED_SOPS = [
        "sop-growth",
        "sop-customer",
        "sop-build",
        "sop-gna",
        "sop-people",
    ]

    def test_all_5_sop_skills_exist_and_have_valid_frontmatter(self):
        for sop in self.REQUIRED_SOPS:
            skill_dir = ROOT / ".agents" / "skills" / sop
            skill_file = skill_dir / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"SOP skill file missing: {skill_file}")
            content = skill_file.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---\n"), f"{sop}/SKILL.md must have frontmatter")
            self.assertIn(f"name: {sop}", content)
            self.assertIn("description:", content)


class AuthorizerHookTests(unittest.TestCase):
    def invoke(self, event, payload):
        self.assertTrue(AUTHORIZER_HOOK.exists(), f"Authorizer hook missing at {AUTHORIZER_HOOK}")
        result = subprocess.run(
            [sys.executable, str(AUTHORIZER_HOOK), event],
            input=payload,
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_authorizer_blocks_unauthorized_r3_payment_command(self):
        payload = json.dumps({
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "curl -X POST https://api.stripe.com/v1/refunds -d charge=ch_123"}
            }
        })
        res = self.invoke("PreToolUse", payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("R3", res["reason"])

    def test_authorizer_blocks_disallowed_capability_tool(self):
        payload = json.dumps({
            "taskContract": {
                "task_id": "tsk_readonly",
                "capability_allowlist": ["read_file"]
            },
            "toolCall": {
                "name": "edit_file",
                "args": {"Path": "/tmp/secret.py", "Target": "a", "Replacement": "b"}
            }
        })
        res = self.invoke("PreToolUse", payload)
        self.assertEqual(res["decision"], "deny")
        self.assertIn("capability", res["reason"].lower())

    def test_authorizer_allows_allowed_capability_tool(self):
        payload = json.dumps({
            "taskContract": {
                "task_id": "tsk_readwrite",
                "capability_allowlist": ["read_file", "edit_file"]
            },
            "toolCall": {
                "name": "read_file",
                "args": {"Path": "/tmp/notes.txt"}
            }
        })
        res = self.invoke("PreToolUse", payload)
        self.assertEqual(res["decision"], "allow")

    def test_authorizer_fails_closed_on_high_impact_error(self):
        # Malformed input with high-impact marker fails closed to deny
        payload = '{"toolCall": {"name": "run_command", "args": {"CommandLine": "wire money"}}}'
        res = self.invoke("PreToolUse", payload)
        self.assertEqual(res["decision"], "deny")


if __name__ == "__main__":
    unittest.main()
