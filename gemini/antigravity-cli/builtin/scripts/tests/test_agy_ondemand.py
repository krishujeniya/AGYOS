"""Tests for AGY On-Demand MCP and Plugin Manager."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import agy_ondemand
from scripts.hooks import authorizer


class AgyOnDemandTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)

        self.mcp_config = self.test_dir / "mcp_config.json"
        self.workspace_mcp = self.test_dir / ".mcp.json"
        self.config_json = self.test_dir / "config.json"

        with open(self.mcp_config, "w", encoding="utf-8") as f:
            json.dump({"mcpServers": {"test-mcp": {"command": "echo", "disabled": False}}}, f)

        with open(self.workspace_mcp, "w", encoding="utf-8") as f:
            json.dump({"mcpServers": {"test-work-mcp": {"command": "echo", "disabled": False}}}, f)

        with open(self.config_json, "w", encoding="utf-8") as f:
            json.dump({"plugins": {"test-plugin": {"enabled": True}}}, f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_disable_and_enable_mcp(self):
        with patch.object(agy_ondemand, "GLOBAL_MCP_CONFIG", self.mcp_config), \
             patch.object(agy_ondemand, "WORKSPACE_MCP_CONFIG", self.workspace_mcp):
            disabled_count = agy_ondemand.disable_all_mcps()
            self.assertGreaterEqual(disabled_count, 1)

            cfg = agy_ondemand.read_json(self.mcp_config)
            self.assertTrue(cfg["mcpServers"]["test-mcp"]["disabled"])

            enabled = agy_ondemand.enable_mcp_server("test-mcp")
            self.assertTrue(enabled)
            cfg_after = agy_ondemand.read_json(self.mcp_config)
            self.assertFalse(cfg_after["mcpServers"]["test-mcp"]["disabled"])

    def test_disable_and_enable_plugin(self):
        with patch.object(agy_ondemand, "GLOBAL_CONFIG", self.config_json), \
             patch.object(agy_ondemand, "get_installed_plugins", return_value=["test-plugin"]):
            disabled_count = agy_ondemand.disable_all_plugins()
            self.assertGreaterEqual(disabled_count, 1)

            cfg = agy_ondemand.read_json(self.config_json)
            self.assertFalse(cfg["plugins"]["test-plugin"]["enabled"])

            enabled = agy_ondemand.enable_plugin_bundle("test-plugin")
            self.assertTrue(enabled)
            cfg_after = agy_ondemand.read_json(self.config_json)
            self.assertTrue(cfg_after["plugins"]["test-plugin"]["enabled"])

    def test_resolve_target_by_tool_and_skill(self):
        kind, name = agy_ondemand.resolve_target("deepnote_run")
        self.assertEqual(kind, "mcp")
        self.assertEqual(name, "deepnote-mcp")

        kind, name = agy_ondemand.resolve_target("verification-loop")
        self.assertEqual(kind, "plugin")
        self.assertEqual(name, "agyos-verification")

    def test_hook_auto_activate_demand(self):
        with patch("scripts.agy_ondemand.enable_mcp_server") as mock_enable:
            authorizer.auto_activate_demand("call_mcp_tool", {"ServerName": "mongodb"})
            mock_enable.assert_called_once_with("mongodb")


if __name__ == "__main__":
    unittest.main()
