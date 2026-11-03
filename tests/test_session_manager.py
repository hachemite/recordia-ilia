"""Unit and integration tests for SessionManager and StepRecord."""

import os
import shutil
import tempfile
import unittest
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from storage.session_manager import SessionManager, StepRecord


class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sm = SessionManager(base_directory=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_start_session_creates_directory_structure(self):
        session_dir = self.sm.start_session("Login_Test")
        self.assertTrue(self.sm.is_active)
        self.assertTrue(session_dir.exists())
        self.assertTrue(self.sm.screenshots_dir.exists())
        self.assertIn("Login_Test", str(session_dir))

    def test_record_steps_with_metadata(self):
        self.sm.start_session("Checkout_Flow")
        img1 = Image.new("RGB", (200, 200), color="blue")
        img2 = Image.new("RGB", (200, 200), color="green")

        step1 = self.sm.record_step(
            img1,
            description="Navigated to Cart",
            window_info={"app_name": "chrome.exe", "window_title": "Shopping Cart", "pid": 1234}
        )
        self.assertEqual(step1.step_number, 1)
        self.assertEqual(step1.app_name, "chrome.exe")
        self.assertEqual(step1.description, "Navigated to Cart")
        self.assertTrue(os.path.exists(step1.image_path))

        step2 = self.sm.record_step(
            img2,
            description="Clicked Checkout",
            window_info={"app_name": "chrome.exe", "window_title": "Payment Portal", "pid": 1234}
        )
        self.assertEqual(step2.step_number, 2)
        self.assertEqual(self.sm.step_count, 2)

    def test_finish_session_generates_html_and_markdown_reports(self):
        self.sm.start_session("Report_Verification")
        img = Image.new("RGB", (100, 100), color="red")
        self.sm.record_step(img, description="Sample test step")

        result = self.sm.finish_session()
        self.assertFalse(self.sm.is_active)
        self.assertEqual(result["step_count"], 1)

        html_report = result["html_report"]
        md_report = result["markdown_report"]
        meta_file = result["metadata_file"]

        self.assertTrue(os.path.exists(html_report))
        self.assertTrue(os.path.exists(md_report))
        self.assertTrue(os.path.exists(meta_file))

        with open(html_report, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("RecordiaILIA Steps Report", content)
            self.assertIn("Sample test step", content)
            self.assertIn("step_01.png", content)

        with open(md_report, "r", encoding="utf-8") as f:
            md_content = f.read()
            self.assertIn("Steps Recording Report", md_content)
            self.assertIn("Sample test step", md_content)


if __name__ == "__main__":
    unittest.main()
