"""
Main entry point for RecordiaILIA application.
Integrates UI, settings, file manager, hotkeys, and capture engines.
"""

import sys
import os

# Ensure src root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from core.hotkeys import HotkeyManager
from storage.file_manager import FileManager
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow


class RecordiaApp:
    def __init__(self):
        self.settings = Settings()
        self.file_manager = FileManager(self.settings.get("save_directory"))
        self.is_recording = False

        # Placeholder callbacks (to be linked with capture engine)
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
        self.window.set_status("Settings updated")

    def _open_captures_folder(self):
        self.file_manager.open_captures_folder()
        self.window.set_status("Opened captures folder")

    def _handle_screenshot(self):
        filepath = self.file_manager.generate_screenshot_path(self.settings.get("screenshot_format", "png"))
        print(f"[Recordia] Screenshot target: {filepath}")

    def _handle_start_record(self):
        filepath = self.file_manager.generate_recording_path(self.settings.get("video_format", "mp4"))
        print(f"[Recordia] Recording started target: {filepath}")
        self.is_recording = True

    def _handle_stop_record(self):
        print("[Recordia] Recording stopped.")
        self.is_recording = False

    def _on_hotkey_screenshot(self):
        print("[Recordia] Hotkey detected: Screenshot")
        self._handle_screenshot()
        self.window.set_status("Screenshot taken (Hotkey)")

    def _on_hotkey_toggle_record(self):
        print("[Recordia] Hotkey detected: Toggle Recording")
        if not self.is_recording:
            self._handle_start_record()
            self.window.set_status("Recording... (Hotkey)")
        else:
            self._handle_stop_record()
            self.window.set_status("Recording stopped (Hotkey)")

    def run(self):
        self.hotkeys.start()
        try:
            self.window.run()
        finally:
            self.cleanup()

    def cleanup(self):
        if hasattr(self, "hotkeys") and self.hotkeys.is_running:
            self.hotkeys.stop()


if __name__ == "__main__":
    app = RecordiaApp()
    app.run()
