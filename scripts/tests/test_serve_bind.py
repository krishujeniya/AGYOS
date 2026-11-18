import os
import unittest
from unittest.mock import patch

from agyos_decision.serve import _resolve_bind_host


class BindHostTests(unittest.TestCase):
    def test_defaults_to_loopback(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(_resolve_bind_host(), "127.0.0.1")

    def test_remote_bind_requires_opt_in_and_key(self):
        with patch.dict(os.environ, {"ROXX_HOST": "0.0.0.0"}, clear=True):
            with self.assertRaises(ValueError):
                _resolve_bind_host()
            os.environ["ROXX_ALLOW_REMOTE"] = "1"
            with self.assertRaises(ValueError):
                _resolve_bind_host()
            os.environ["ROXX_API_KEY"] = "test-key"
            self.assertEqual(_resolve_bind_host(), "0.0.0.0")
