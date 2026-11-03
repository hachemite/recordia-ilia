"""Unit tests for Settings configuration module."""

import os
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from config.settings import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.settings = Settings(config_path=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_default_values(self):
        self.assertEqual(self.settings.get("screenshot_format"), "png")
        self.assertEqual(self.settings.get("video_fps"), 30)
        self.assertIn("screenshot", self.settings.get("hotkeys"))

    def test_set_and_save_persistence(self):
        self.settings.set("video_fps", 60)
        self.settings.set("screenshot_format", "jpg")

        # Reload in fresh instance
        reloaded = Settings(config_path=self.temp_file.name)
        self.assertEqual(reloaded.get("video_fps"), 60)
        self.assertEqual(reloaded.get("screenshot_format"), "jpg")


if __name__ == "__main__":
    unittest.main()
