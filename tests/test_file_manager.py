"""Unit tests for FileManager module."""

import os
import shutil
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from storage.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fm = FileManager(base_directory=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_directory_creation(self):
        self.assertTrue(os.path.isdir(self.fm.screenshots_dir))
        self.assertTrue(os.path.isdir(self.fm.recordings_dir))

    def test_generate_screenshot_path(self):
        path_png = self.fm.generate_screenshot_path("png")
        self.assertTrue(path_png.endswith(".png"))
        self.assertIn("screenshot_", path_png)

        path_jpg = self.fm.generate_screenshot_path("jpg")
        self.assertTrue(path_jpg.endswith(".jpg"))

    def test_generate_recording_path(self):
        path_mp4 = self.fm.generate_recording_path("mp4")
        self.assertTrue(path_mp4.endswith(".mp4"))
        self.assertIn("recording_", path_mp4)

    def test_update_base_directory(self):
        new_dir = os.path.join(self.test_dir, "custom_captures")
        self.fm.set_base_directory(new_dir)
        self.assertEqual(str(self.fm.base_dir), new_dir)
        self.assertTrue(os.path.isdir(self.fm.screenshots_dir))


if __name__ == "__main__":
    unittest.main()
