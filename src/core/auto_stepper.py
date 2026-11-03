"""
Automated step trigger engine for RecordiaILIA.
Supports event-driven triggers:
- Manual (Hotkey / Button)
- On Mouse Click (captures every user click with coordinates)
- Periodic Interval Timer (captures every N seconds)
"""

import threading
import time
from enum import Enum
from typing import Callable, Optional, Dict, Any
from pynput import mouse


class TriggerMode(str, Enum):
    MANUAL = "manual"
    ON_CLICK = "on_click"
    PERIODIC = "periodic"


class AutoStepper:
    """
    Manages automated step capturing via mouse click events or periodic interval timers.
    """

    def __init__(self, step_trigger_callback: Callable[[str, Dict[str, Any]], None]):
        """
        :param step_trigger_callback: Function called when a trigger fires.
                                      Signature: callback(description: str, meta: dict)
        """
        self.callback = step_trigger_callback
        self.mode = TriggerMode.MANUAL
        self.interval = 3.0
        self._is_running = False

        self._mouse_listener: Optional[mouse.Listener] = None
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._last_click_time = 0.0
        self._debounce_seconds = 0.35
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        return self._is_running

    def start(self, mode: TriggerMode, interval_seconds: float = 3.0):
        """
        Starts automated capture in the specified mode.
        """
        with self._lock:
            if self._is_running:
                self.stop()

            self.mode = mode
            self.interval = max(0.5, float(interval_seconds))
            self._is_running = True
            self._stop_event.clear()

            if self.mode == TriggerMode.ON_CLICK:
                self._start_mouse_listener()
            elif self.mode == TriggerMode.PERIODIC:
                self._start_timer_thread()

    def stop(self):
        """
        Stops any active automated listeners or timer threads.
        """
        with self._lock:
            if not self._is_running:
                return

            self._is_running = False
            self._stop_event.set()

            if self._mouse_listener:
                try:
                    self._mouse_listener.stop()
                except Exception as e:
                    print(f"[AutoStepper] Error stopping mouse listener: {e}")
                self._mouse_listener = None

            if self._timer_thread and self._timer_thread.is_alive():
                self._timer_thread.join(timeout=2.0)
                self._timer_thread = None

    def _start_mouse_listener(self):
        """Starts pynput mouse click listener."""
        try:
            self._mouse_listener = mouse.Listener(on_click=self._on_mouse_click)
            self._mouse_listener.daemon = True
            self._mouse_listener.start()
        except Exception as e:
            print(f"[AutoStepper] Failed to start mouse listener: {e}")
            self._is_running = False

    def _on_mouse_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        """Callback for mouse clicks."""
        if not pressed or not self._is_running:
            return

        now = time.time()
        # Debounce rapid clicks
        if now - self._last_click_time < self._debounce_seconds:
            return
        self._last_click_time = now

        btn_name = "Left Click" if "left" in str(button).lower() else ("Right Click" if "right" in str(button).lower() else "Click")
        desc = f"Mouse {btn_name} at ({x}, {y})"
        meta = {
            "trigger_type": "mouse_click",
            "x": x,
            "y": y,
            "button": str(button)
        }

        # Fire step trigger in a separate thread to prevent blocking mouse hook
        threading.Thread(target=self.callback, args=(desc, meta), daemon=True).start()

    def _start_timer_thread(self):
        """Starts periodic capture loop thread."""
        self._timer_thread = threading.Thread(target=self._periodic_loop, daemon=True)
        self._timer_thread.start()

    def _periodic_loop(self):
        """Background loop triggering steps at fixed time intervals."""
        tick = 1
        while self._is_running and not self._stop_event.is_set():
            time.sleep(self.interval)
            if not self._is_running or self._stop_event.is_set():
                break

            desc = f"Periodic capture interval #{tick} ({self.interval:.1f}s)"
            meta = {
                "trigger_type": "periodic_timer",
                "interval": self.interval,
                "tick": tick
            }
            tick += 1
            self.callback(desc, meta)
