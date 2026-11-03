"""
Main entry point for RecordiaILIA application.
Integrates UI, settings, file manager, hotkeys, screenshot, and screen recording engines.
"""

import sys
import os

# Ensure src root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from core.hotkeys import HotkeyManager
from storage.file_manager import FileManager
from capture.screenshot import ScreenshotEngine
from capture.recorder import ScreenRecorder
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow


class RecordiaApp:
    def __init__(self):
        self.settings = Settings()
        self.file_manager = FileManager(self.settings.get("save_directory"))
        self.screenshot_engine = ScreenshotEngine(
            self.file_manager,
            default_format=self.settings.get("screenshot_format", "png")
        )
        self.recorder = ScreenRecorder(
            self.file_manager,
            fps=int(self.settings.get("video_fps", 30)),
            video_format=self.settings.get("video_format", "mp4")
        )

        # Callbacks
        self.screenshot_callback = self._handle_screenshot
        self.start_record_callback = self._handle_start_record
        self.stop_record_callback = self._handle_stop_record

        # Initialize UI
        self.window = MainWindow(
            on_screenshot=self.screenshot_callback,
            on_start_record=self.start_record_callback,
            on_stop_record=self.stop_record_callback,
            on_open_settings=self._open_settings,
            on_open_captures=self._open_captures_folder,
            on_close=self.cleanup
        )

        # Initialize hotkey manager
        hotkey_bindings = {
            self.settings.get("hotkeys", {}).get("screenshot", "<ctrl>+<shift>+s"): self._on_hotkey_screenshot,
            self.settings.get("hotkeys", {}).get("toggle_record", "<ctrl>+<shift>+r"): self._on_hotkey_toggle_record
        }
        self.hotkeys = HotkeyManager(hotkey_bindings)

    def _open_settings(self):
        SettingsWindow(self.window.root, self.settings, on_save=self._on_settings_updated)

    def _on_settings_updated(self):
        new_dir = self.settings.get("save_directory")
        self.file_manager.set_base_directory(new_dir)
        self.screenshot_engine.default_format = self.settings.get("screenshot_format", "png")
        self.recorder.fps = int(self.settings.get("video_fps", 30))
        self.window.set_status("Settings updated")

    def _open_captures_folder(self):
        self.file_manager.open_captures_folder()
        self.window.set_status("Opened captures folder")

    def _handle_screenshot(self) -> str:
        fmt = self.settings.get("screenshot_format", "png")
        saved_file = self.screenshot_engine.capture_fullscreen(fmt=fmt)
        filename = os.path.basename(saved_file)
        print(f"[Recordia] Screenshot saved to: {saved_file}")
        self.window.set_status(f"Saved: {filename}")
        return saved_file

    def _handle_start_record(self):
        if not self.recorder.is_recording:
            target = self.recorder.start_recording()
            print(f"[Recordia] Recording started target: {target}")
            self.window.set_status("Recording in progress...")

    def _handle_stop_record(self):
        if self.recorder.is_recording:
            saved_file = self.recorder.stop_recording()
            filename = os.path.basename(saved_file)
            print(f"[Recordia] Recording saved to: {saved_file}")
            self.window.set_status(f"Video saved: {filename}")
        else:
            self.window.set_status("Ready")

    def _on_hotkey_screenshot(self):
        print("[Recordia] Hotkey detected: Screenshot")
        saved_file = self._handle_screenshot()
        filename = os.path.basename(saved_file)
        self.window.set_status(f"Saved: {filename} (Hotkey)")

    def _on_hotkey_toggle_record(self):
        print("[Recordia] Hotkey detected: Toggle Recording")
        if not self.recorder.is_recording:
            self._handle_start_record()
        else:
            self._handle_stop_record()

    def run(self):
        self.hotkeys.start()
        try:
            self.window.run()
        finally:
            self.cleanup()

    def cleanup(self):
        if hasattr(self, "recorder") and self.recorder.is_recording:
            self.recorder.stop_recording()
        if hasattr(self, "hotkeys") and self.hotkeys.is_running:
            self.hotkeys.stop()


if __name__ == "__main__":
    app = RecordiaApp()
    app.run()
