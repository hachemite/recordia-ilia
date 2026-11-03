"""
Utility for inspecting active foreground window and process details.
"""

import os
import sys
from typing import Dict, Any

try:
    import psutil
except ImportError:
    psutil = None


def get_active_window_info() -> Dict[str, Any]:
    """
    Detects the currently active foreground window title and executable name.
    Returns a dictionary with keys:
        - 'app_name': Process/application executable name (e.g. 'chrome.exe', 'Code.exe')
        - 'window_title': Title text of the window
        - 'pid': Process ID
    """
    default_info = {
        "app_name": "Desktop",
        "window_title": "Desktop Workspace",
        "pid": 0
    }

    if sys.platform != "win32":
        return default_info

    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            return default_info

        # Retrieve window title text
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value.strip() or "Active Window"
        else:
            title = "Active Window"

        # Retrieve process ID and executable name
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process_id = pid.value

        app_name = "Application"
        if psutil and process_id > 0:
            try:
                proc = psutil.Process(process_id)
                app_name = proc.name()
            except Exception:
                app_name = f"Process_{process_id}"

        return {
            "app_name": app_name,
            "window_title": title,
            "pid": process_id
        }
    except Exception as e:
        return {
            "app_name": "Unknown",
            "window_title": f"Captured Window ({e})",
            "pid": 0
        }
