"""
Application configuration and default settings.
"""

import json
import os
from pathlib import Path


class Settings:
    """Manages application settings, paths, and default hotkeys."""

    DEFAULT_SETTINGS = {
        "save_directory": str(Path.home() / "Pictures" / "RecordiaCaptures"),
        "screenshot_format": "png",
        "video_fps": 30,
        "video_format": "mp4",
        "hotkeys": {
            "screenshot": "<ctrl>+<shift>+s",
            "toggle_record": "<ctrl>+<shift>+r"
        }
    }

    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "settings.json"
        )
        self.data = dict(self.DEFAULT_SETTINGS)
        self.load()

    def load(self):
        """Load configuration from JSON file if available."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.data.update(saved)
            except Exception as e:
                print(f"[Settings] Error loading config: {e}")

    def save(self):
        """Persist settings to disk."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"[Settings] Error saving config: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
