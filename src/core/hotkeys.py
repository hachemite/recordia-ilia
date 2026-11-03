"""
Global hotkey manager using pynput.
Runs a background listener for defined key combinations.
"""

import threading
from typing import Callable, Dict
from pynput import keyboard


class HotkeyManager:
    """
    Manages global keyboard shortcuts across the operating system.
    """

    def __init__(self, key_bindings: Dict[str, Callable] = None):
        """
        :param key_bindings: Dictionary mapping hotkey combinations to functions.
                             Example: {'<ctrl>+<shift>+s': on_screenshot}
        """
        self.key_bindings = key_bindings or {}
        self._listener = None
        self._is_running = False
        self._last_error: str = ""

    @property
    def last_error(self) -> str:
        """Human-readable message describing the last registration/start failure ("" if none)."""
        return self._last_error

    def register_hotkey(self, combo: str, callback: Callable):
        """Register or overwrite a hotkey combination."""
        self.key_bindings[combo] = callback
        if self._is_running:
            # Restart listener to apply new combination
            self.stop()
            self.start()

    def start(self):
        """Starts listening for global hotkeys in a daemon thread."""
        if self._is_running or not self.key_bindings:
            return

        try:
            self._listener = keyboard.GlobalHotKeys(self.key_bindings)
            self._listener.start()
            self._is_running = True
            self._last_error = ""
        except Exception as e:
            self._last_error = str(e)
            print(f"[HotkeyManager] Error initializing hotkeys: {e}")
            self._is_running = False

    def stop(self):
        """Stops the global hotkey listener cleanly."""
        if self._listener and self._is_running:
            try:
                self._listener.stop()
            except Exception as e:
                print(f"[HotkeyManager] Error stopping listener: {e}")
            finally:
                self._listener = None
                self._is_running = False

    @property
    def is_running(self) -> bool:
        return self._is_running
