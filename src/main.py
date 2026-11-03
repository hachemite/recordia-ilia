"""
Main entry point for RecordiaILIA application.
Integrates UI, automated step recording, step description review editor,
settings with custom hotkey configuration, file manager, and video recording.
"""

import sys
import os
import webbrowser
from tkinter import messagebox

# Ensure src root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from core.hotkeys import HotkeyManager
from core.window_info import get_active_window_info
from core.auto_stepper import AutoStepper, TriggerMode
from storage.file_manager import FileManager
from storage.session_manager import SessionManager
from capture.screenshot import ScreenshotEngine
from capture.recorder import ScreenRecorder
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow
from ui.step_dialog import StepDialog
from ui.step_editor_window import StepEditorWindow


class RecordiaApp:
    def __init__(self):
        self.settings = Settings()
        self.save_dir = self.settings.get("save_directory")
        self.file_manager = FileManager(self.save_dir)
        self.session_manager = SessionManager(self.save_dir)

        self.screenshot_engine = ScreenshotEngine(
            self.file_manager,
            default_format=self.settings.get("screenshot_format", "png")
        )
        self.recorder = ScreenRecorder(
            self.file_manager,
            fps=int(self.settings.get("video_fps", 30)),
            video_format=self.settings.get("video_format", "mp4")
        )

        self.auto_stepper = AutoStepper(step_trigger_callback=self._on_auto_trigger)
        self.quick_mode = False

        # Load hotkeys
        current_hotkeys = self.settings.get("hotkeys", {})
        self.step_hotkey = current_hotkeys.get("screenshot", "<ctrl>+<shift>+s")
        self.video_hotkey = current_hotkeys.get("toggle_record", "<ctrl>+<shift>+r")

        # Initialize UI
        self.window = MainWindow(
            on_record_step=self._handle_record_step,
            on_finish_session=self._handle_finish_session,
            on_toggle_auto=self._handle_toggle_auto,
            on_open_step_editor=self._open_step_editor,
            on_screenshot=self._handle_screenshot,
            on_start_record=self._handle_start_record,
            on_stop_record=self._handle_stop_record,
            on_open_settings=self._open_settings,
            on_open_captures=self._open_captures_folder,
            on_close=self.cleanup,
            step_hotkey=self.step_hotkey,
            video_hotkey=self.video_hotkey
        )

        # Initialize hotkey manager
        hotkey_bindings = {
            self.step_hotkey: self._on_hotkey_record_step,
            self.video_hotkey: self._on_hotkey_toggle_record
        }
        self.hotkeys = HotkeyManager(hotkey_bindings)

    def _open_settings(self):
        SettingsWindow(self.window.root, self.settings, on_save=self._on_settings_updated)

    def _open_step_editor(self):
        if self.session_manager.step_count == 0:
            self.window.set_status("No steps in session to review yet.")
            return
        StepEditorWindow(self.window.root, self.session_manager, on_updated=self._on_step_updated)

    def _on_step_updated(self):
        self.window.set_status("Step description updated in session.")

    def _on_settings_updated(self):
        new_dir = self.settings.get("save_directory")
        self.file_manager.set_base_directory(new_dir)
        self.session_manager.base_dir = self.file_manager.base_dir
        self.screenshot_engine.default_format = self.settings.get("screenshot_format", "png")
        self.recorder.fps = int(self.settings.get("video_fps", 30))

        # Dynamically apply new hotkeys
        current_hotkeys = self.settings.get("hotkeys", {})
        self.step_hotkey = current_hotkeys.get("screenshot", "<ctrl>+<shift>+s")
        self.video_hotkey = current_hotkeys.get("toggle_record", "<ctrl>+<shift>+r")

        if hasattr(self, "hotkeys"):
            self.hotkeys.stop()
            self.hotkeys.key_bindings = {
                self.step_hotkey: self._on_hotkey_record_step,
                self.video_hotkey: self._on_hotkey_toggle_record
            }
            self.hotkeys.start()

        self.window.update_hotkey_labels(self.step_hotkey, self.video_hotkey)
        self.window.set_status("Settings and custom hotkeys updated")
        print(f"[Recordia] Hotkeys re-registered: Step={self.step_hotkey}, Video={self.video_hotkey}")

    def _open_captures_folder(self):
        if self.session_manager.current_session_dir and os.path.exists(self.session_manager.current_session_dir):
            target = str(self.session_manager.current_session_dir)
            if sys.platform == "win32":
                os.startfile(target)
            else:
                self.file_manager.open_captures_folder()
        else:
            self.file_manager.open_captures_folder()
        self.window.set_status("Opened captures folder")

    def _handle_record_step(self):
        """Captures a single manual step with optional dialog prompt."""
        if not self.session_manager.is_active:
            proj_name = self.window.get_project_name()
            self.session_manager.start_session(proj_name)

        window_info = get_active_window_info()
        next_step = self.session_manager.step_count + 1
        image = self.screenshot_engine._grab_screen()

        desc = ""
        if not self.quick_mode:
            dialog = StepDialog(self.window.root, next_step, window_info)
            if dialog.result is None:
                self.window.set_status("Step capture cancelled")
                return
            desc = dialog.result
            if dialog.quick_mode:
                self.quick_mode = True

        step = self.session_manager.record_step(image, description=desc, window_info=window_info)
        self.window.update_step_count(self.session_manager.step_count)
        self.window.set_status(f"Step #{step.step_number} saved: {step.app_name}")
        print(f"[Recordia] Manual Step #{step.step_number} in {step.app_name} ({step.timestamp})")

    def _on_auto_trigger(self, description: str, meta: dict):
        """Background callback invoked automatically by AutoStepper on click or timer."""
        if not self.session_manager.is_active:
            proj_name = self.window.get_project_name()
            self.session_manager.start_session(proj_name)

        window_info = get_active_window_info()
        image = self.screenshot_engine._grab_screen()

        step = self.session_manager.record_step(image, description=description, window_info=window_info)
        self.window.update_step_count(self.session_manager.step_count)
        self.window.set_status(f"Auto Step #{step.step_number}: {step.app_name} - {description}")
        print(f"[Recordia] Auto Step #{step.step_number} ({step.app_name}): {description}")

    def _handle_toggle_auto(self, mode: str, interval: float):
        """Starts or stops automated background step recording."""
        if mode == "stop":
            self.auto_stepper.stop()
            self.window.set_status("Auto-recording stopped")
            print("[Recordia] Auto-recording stopped.")
        else:
            if not self.session_manager.is_active:
                proj_name = self.window.get_project_name()
                self.session_manager.start_session(proj_name)

            trig_mode = TriggerMode.ON_CLICK if mode == "on_click" else TriggerMode.PERIODIC
            self.auto_stepper.start(trig_mode, interval_seconds=interval)
            self.window.set_status(f"Auto-recording active [{trig_mode.value}]")
            print(f"[Recordia] Auto-recording started in mode '{trig_mode.value}' (interval={interval}s).")

    def _handle_finish_session(self):
        """Finalizes step session, compiles HTML report, and opens it."""
        if self.auto_stepper.is_running:
            self.auto_stepper.stop()

        if not self.session_manager.is_active or self.session_manager.step_count == 0:
            self.window.set_status("No steps recorded in active session.")
            return

        res = self.session_manager.finish_session()
        html_report = res.get("html_report")
        count = res.get("step_count", 0)

        self.window.set_status(f"Session finished ({count} steps). Report generated!")
        print(f"[Recordia] Session finished. Report: {html_report}")

        if html_report and os.path.exists(html_report):
            webbrowser.open(f"file:///{html_report}")

        self.quick_mode = False
        self.window.update_step_count(0)

    def _handle_screenshot(self) -> str:
        fmt = self.settings.get("screenshot_format", "png")
        saved_file = self.screenshot_engine.capture_fullscreen(fmt=fmt)
        filename = os.path.basename(saved_file)
        self.window.set_status(f"Saved: {filename}")
        return saved_file

    def _handle_start_record(self):
        if not self.recorder.is_recording:
            target = self.recorder.start_recording()
            print(f"[Recordia] Video recording started: {target}")
            self.window.set_status("Recording video...")

    def _handle_stop_record(self):
        if self.recorder.is_recording:
            saved_file = self.recorder.stop_recording()
            filename = os.path.basename(saved_file)
            print(f"[Recordia] Video saved: {saved_file}")
            self.window.set_status(f"Video saved: {filename}")
        else:
            self.window.set_status("Ready")

    def _on_hotkey_record_step(self):
        print("[Recordia] Hotkey detected: Step Capture")
        self._handle_record_step()

    def _on_hotkey_toggle_record(self):
        print("[Recordia] Hotkey detected: Toggle Video")
        if not self.recorder.is_recording:
            self._handle_start_record()
        else:
            self._handle_stop_record()

    def run(self):
        self.hotkeys.start()
        if not self.hotkeys.is_running and self.hotkeys.last_error:
            warning = (
                "Global hotkeys could not be registered:\n"
                f"{self.hotkeys.last_error}\n\n"
                "Step capture and video hotkeys will be inactive. "
                "You can still use the buttons in this window."
            )
            messagebox.showwarning("Hotkey Registration Failed", warning)
            self.window.set_status("Warning: global hotkeys are inactive")
        try:
            self.window.run()
        finally:
            self.cleanup()

    def cleanup(self):
        if hasattr(self, "auto_stepper") and self.auto_stepper.is_running:
            self.auto_stepper.stop()
        if hasattr(self, "recorder") and self.recorder.is_recording:
            self.recorder.stop_recording()
        if hasattr(self, "hotkeys") and self.hotkeys.is_running:
            self.hotkeys.stop()


if __name__ == "__main__":
    app = RecordiaApp()
    app.run()
