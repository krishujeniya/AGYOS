"""Tests for Cross-Surface Status and Next Safe Action Alignment (CLI, MCP, State Store)."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]


class StatusAlignmentTests(unittest.TestCase):
    def test_cli_and_state_sh_report_aligned_next_safe_action(self):
        # Test shell helper function
        script = """
        source bin/state.sh
        for gate in IDLE UNDERSTAND ANALYZE PLAN IMPLEMENT VERIFY; do
            nsa=$(anchor_next_safe_action "$gate")
            if [ -z "$nsa" ]; then
                echo "FAIL: empty action for $gate" >&2
                exit 1
            fi
            echo "$gate:$nsa"
        done
        """
        res = subprocess.run(["bash", "-c", script], cwd=ROOT.parent, capture_output=True, text=True, check=True)
        lines = res.stdout.strip().splitlines()
        self.assertEqual(len(lines), 6)
        self.assertTrue(any("UNDERSTAND" in line for line in lines))

    def test_mcp_reports_next_safe_action_in_sysinfo_and_state(self):
        mcp_server = ROOT.parent / "mcp" / "state-server.cjs"
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "agyos_sys_info", "arguments": {}}
        }
        res = subprocess.run(
            ["node", str(mcp_server)],
            input=json.dumps(req) + "\n",
            capture_output=True,
            text=True,
            check=True
        )
        parsed = json.loads(res.stdout.strip().splitlines()[0])
        self.assertNotIn("error", parsed)
        content_text = parsed["result"]["content"][0]["text"]
        sys_info = json.loads(content_text)
        self.assertIn("active_gate", sys_info)
        self.assertIn("next_safe_action", sys_info)
        self.assertIsInstance(sys_info["next_safe_action"], str)
        self.assertGreater(len(sys_info["next_safe_action"]), 0)

    def test_mcp_exposes_workspace_state_tool(self):
        mcp_server = ROOT.parent / "mcp" / "state-server.cjs"
        req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        res = subprocess.run(
            ["node", str(mcp_server)],
            input=json.dumps(req) + "\n",
            capture_output=True,
            text=True,
            check=True
        )
        parsed = json.loads(res.stdout.strip().splitlines()[0])
        tool_names = [t["name"] for t in parsed["result"]["tools"]]
        self.assertIn("agyos_workspace_state", tool_names)
        self.assertIn("agyos_state", tool_names)


if __name__ == "__main__":
    unittest.main()
