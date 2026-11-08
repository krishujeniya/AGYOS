"""Offline regressions for AGY startup metadata and lifecycle hook responses."""

import json
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "scripts/hooks/agy_os_hook.py"


class HookContractTests(unittest.TestCase):
    def invoke(self, event, payload):
        result = subprocess.run(
            [sys.executable, str(HOOK), event],
            input=payload,
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_pre_tool_denies_dangerous_real_cli_payload(self):
        payload = json.dumps({
            "toolCall": {"name": "run_command", "args": {"CommandLine": "rm -rf /"}}
        })
        self.assertEqual(self.invoke("PreToolUse", payload)["decision"], "deny")

    def test_pre_tool_allows_benign_command(self):
        payload = json.dumps({
            "toolCall": {"name": "run_command", "args": {"CommandLine": "npm test"}}
        })
        self.assertEqual(self.invoke("PreToolUse", payload), {"decision": "allow"})

    def test_non_decision_events_return_empty_objects(self):
        for event in ("PreInvocation", "PostInvocation", "PostToolUse"):
            with self.subTest(event=event):
                self.assertEqual(self.invoke(event, "{}"), {})

    def test_empty_and_malformed_input_follow_event_contract(self):
        for payload in ("", "{", "null", "[]"):
            for event in ("PreToolUse", "PostToolUse", "PreInvocation", "PostInvocation"):
                expected = {"decision": "deny"} if event == "PreToolUse" else {}
                with self.subTest(event=event, payload=payload):
                    result = self.invoke(event, payload)
                    self.assertEqual(result.get("decision"), "deny") if event == "PreToolUse" else self.assertEqual(result, expected)

    def test_stop_allows_termination(self):
        self.assertEqual(self.invoke("Stop", '{"fullyIdle":true}'), {"decision": "allow"})

    def test_legacy_payload_still_denies_dangerous_command(self):
        payload = json.dumps({"tool_input": {"command": "mkfs /dev/sda"}})
        self.assertEqual(self.invoke("PreToolUse", payload)["decision"], "deny")

    def test_invalid_command_type_does_not_emit_unknown_warning_field(self):
        payload = json.dumps({"toolCall": {"args": {"CommandLine": ["npm", "test"]}}})
        self.assertEqual(self.invoke("PreToolUse", payload)["decision"], "deny")


class StartupMetadataTests(unittest.TestCase):
    def test_attune_skill_is_text_with_its_documented_assets(self):
        base = ROOT / ".agents/skills/attune-task-bridge"
        self.assertTrue((base / "SKILL.md").read_text().startswith("---\n"))
        for asset in ("references/api.md", "scripts/check_tasks.py", "scripts/ws_bridge.py",
                      "scripts/poll_tasks.py", "scripts/notify.py"):
            with self.subTest(asset=asset):
                self.assertTrue((base / asset).is_file())

    def test_planning_header_has_no_embedded_delimiter(self):
        text = (ROOT / ".agents/skills/planning-with-files/SKILL.md").read_text()
        header = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)[1]
        self.assertNotIn("---", header)

    def test_every_flat_rule_declares_supported_trigger(self):
        for path in (ROOT / ".agents/rules").glob("*.md"):
            with self.subTest(path=path.name):
                header = path.read_text().split("---", 2)
                self.assertEqual(header[0].strip(), "")
                self.assertRegex(header[1], r"(?m)^trigger: (always_on|model_decision|glob|manual)$")

    def test_workflow_directory_contains_only_loadable_markdown(self):
        for path in (ROOT / ".agents/workflows").glob("*.md"):
            with self.subTest(path=path.name):
                self.assertTrue(path.read_text().startswith("---\n"))


class NotificationTests(unittest.TestCase):
    def test_macos_task_text_is_data_instead_of_applescript(self):
        path = ROOT / ".agents/skills/attune-task-bridge/scripts/notify.py"
        spec = importlib.util.spec_from_file_location("attune_notify", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        title = 'Task "quoted"\nset malicious to true'
        message = 'Text with \\ and "quotes"'
        with patch.object(module.subprocess, "run") as run:
            self.assertTrue(module.notify_macos(title, message, sound=False))
        args = run.call_args.args[0]
        self.assertEqual(args[:2], ["osascript", "-e"])
        self.assertNotIn(title, args[2])
        self.assertNotIn(message, args[2])
        self.assertEqual(args[-3:], [title, message, "false"])


if __name__ == "__main__":
    unittest.main()
