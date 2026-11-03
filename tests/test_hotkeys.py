"""Unit tests for HotkeyManager module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from core.hotkeys import HotkeyManager


class TestHotkeyManager(unittest.TestCase):
    def test_init_and_bindings(self):
        called = []
        dummy_cb = lambda: called.append(True)
        hm = HotkeyManager({"<ctrl>+<alt>+z": dummy_cb})
        self.assertIn("<ctrl>+<alt>+z", hm.key_bindings)
        self.assertFalse(hm.is_running)

    def test_register_hotkey(self):
        hm = HotkeyManager()
        self.assertEqual(len(hm.key_bindings), 0)
        hm.register_hotkey("<ctrl>+k", lambda: None)
        self.assertIn("<ctrl>+k", hm.key_bindings)

    def test_stop_when_not_started(self):
        hm = HotkeyManager()
        # Should not raise exception
        hm.stop()
        self.assertFalse(hm.is_running)


if __name__ == "__main__":
    unittest.main()
