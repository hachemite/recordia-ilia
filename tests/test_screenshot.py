"""Unit and integration tests for ScreenshotEngine."""

import os
import shutil
import tempfile
import unittest
import unittest.mock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from storage.file_manager import FileManager
from capture.screenshot import ScreenshotEngine


class TestScreenshotEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fm = FileManager(base_directory=self.test_dir)
        self.engine = ScreenshotEngine(self.fm, default_format="png")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_capture_fullscreen(self):
        saved_path = self.engine.capture_fullscreen()
        self.assertTrue(os.path.exists(saved_path))
        self.assertGreater(os.path.getsize(saved_path), 0)
        self.assertTrue(saved_path.endswith(".png"))

    def test_capture_region(self):
        saved_path = self.engine.capture_region(bbox=(10, 10, 200, 200))
        self.assertTrue(os.path.exists(saved_path))
        self.assertGreater(os.path.getsize(saved_path), 0)

    def test_capture_fails_loudly_when_backends_unavailable(self):
        """Issue #9: no fake fallback image; RuntimeError must be raised."""
        with unittest.mock.patch("PIL.ImageGrab.grab", side_effect=OSError("no display")), \
             unittest.mock.patch("capture.screenshot.mss.MSS", side_effect=OSError("no mss")):
            with self.assertRaises(RuntimeError):
                self.engine.capture_fullscreen()


if __name__ == "__main__":
    unittest.main()
