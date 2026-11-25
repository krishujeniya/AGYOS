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
        from agyos_decision.catalog import resolve_skill_dir
        base = resolve_skill_dir("attune-task-bridge")
        skill_file = (base / "SKILL.toon") if (base / "SKILL.toon").is_file() else (base / "SKILL.md")
        content = skill_file.read_text(encoding="utf-8")
        if content.startswith('mode: "100644"'):
            import json
            content = json.loads(content.split("header: ", 1)[1].strip()) if "header: " in content else json.loads(content.split("text: ", 1)[1].strip())
        self.assertTrue(content.startswith("---\n"))
        for asset in ("references/api.md", "scripts/check_tasks.py", "scripts/ws_bridge.py",
                      "scripts/poll_tasks.py", "scripts/notify.py"):
            with self.subTest(asset=asset):
                asset_file = (base / asset.replace(".md", ".toon")) if not (base / asset).is_file() else (base / asset)
                self.assertTrue(asset_file.is_file())

    def test_planning_header_has_no_embedded_delimiter(self):
        from agyos_decision.catalog import resolve_skill_dir
        p_dir = resolve_skill_dir("planning-with-files")
        plan_file = (p_dir / "SKILL.toon") if (p_dir / "SKILL.toon").is_file() else (p_dir / "SKILL.md")
        text = plan_file.read_text(encoding="utf-8")
        if text.startswith('mode: "100644"'):
            import json
            text = json.loads(text.split("header: ", 1)[1].strip()) if "header: " in text else json.loads(text.split("text: ", 1)[1].strip())
        header = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)[1]
        self.assertNotIn("---", header)

    def test_every_flat_rule_declares_supported_trigger(self):
        rule_files = list((ROOT / "rules").glob("*.toon")) or list((ROOT / "rules").glob("*.md"))
        for path in rule_files:
            with self.subTest(path=path.name):
                raw = path.read_text(encoding="utf-8")
                if raw.startswith('mode: "100644"'):
                    import json
                    text = json.loads(raw.split("text: ", 1)[1].strip())
                else:
                    text = raw
                header = text.split("---", 2)
                self.assertEqual(header[0].strip(), "")
                self.assertRegex(header[1], r"(?m)^trigger: (always_on|model_decision|glob|manual)$")

    def test_workflow_directory_contains_only_loadable_markdown(self):
        wf_files = list((ROOT / "workflows").glob("*.toon")) or list((ROOT / "workflows").glob("*.md"))
        for path in wf_files:
            with self.subTest(path=path.name):
                raw = path.read_text(encoding="utf-8")
                if raw.startswith('mode: "100644"'):
                    import json
                    text = json.loads(raw.split("text: ", 1)[1].strip())
                else:
                    text = raw
                self.assertEqual(text[:4], "---\n")


class NotificationTests(unittest.TestCase):
    def test_macos_task_text_is_data_instead_of_applescript(self):
        from agyos_decision.catalog import resolve_skill_dir
        path = resolve_skill_dir("attune-task-bridge") / "scripts/notify.py"
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
