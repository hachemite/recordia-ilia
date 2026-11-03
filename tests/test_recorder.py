"""Unit and integration tests for ScreenRecorder."""

import os
import shutil
import tempfile
import time
import unittest
import unittest.mock
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from storage.file_manager import FileManager
from capture.recorder import ScreenRecorder


class TestScreenRecorder(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.fm = FileManager(base_directory=self.test_dir)
        self.recorder = ScreenRecorder(self.fm, fps=15, video_format="mp4")

    def tearDown(self):
        if self.recorder.is_recording:
            self.recorder.stop_recording()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_start_and_stop_recording(self):
        self.assertFalse(self.recorder.is_recording)
        target = self.recorder.start_recording()
        self.assertTrue(self.recorder.is_recording)
        self.assertTrue(target.endswith(".mp4"))

        time.sleep(0.8)
        saved = self.recorder.stop_recording()
        self.assertFalse(self.recorder.is_recording)
        self.assertEqual(target, saved)
        self.assertTrue(os.path.exists(saved))
        self.assertGreater(os.path.getsize(saved), 0)

    def test_recorder_thread_terminates_on_stop(self):
        """Issue #10: stop_recording must wait for the worker thread to end."""
        self.recorder.start_recording()
        time.sleep(0.3)
        self.recorder.stop_recording()
        self.assertFalse(self.recorder._thread.is_alive())

    def test_fails_loudly_when_video_writer_cannot_open(self):
        """Issue #10: RuntimeError instead of silently writing no frames."""
        fake_writer = unittest.mock.MagicMock()
        fake_writer.isOpened.return_value = False
        with unittest.mock.patch("cv2.VideoWriter", return_value=fake_writer), \
             unittest.mock.patch("capture.recorder.mss.MSS") as mock_mss:
            mock_mss.return_value.__enter__.return_value.monitors = [{"width": 800, "height": 600}]
            self.recorder.start_recording()
            with self.assertRaises(RuntimeError):
                self.recorder.stop_recording()


if __name__ == "__main__":
    unittest.main()
