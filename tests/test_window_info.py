"""Unit tests for window_info utility."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from core.window_info import get_active_window_info


class TestWindowInfo(unittest.TestCase):
    def test_get_active_window_info_structure(self):
        info = get_active_window_info()
        self.assertIsInstance(info, dict)
        self.assertIn("app_name", info)
        self.assertIn("window_title", info)
        self.assertIn("pid", info)
        self.assertTrue(len(info["app_name"]) > 0)
        self.assertTrue(len(info["window_title"]) > 0)


if __name__ == "__main__":
    unittest.main()
