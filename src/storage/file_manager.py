"""
File and directory management for saving screenshots and recordings.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class FileManager:
    """Manages file naming, directory structure, and retrieval for captures."""

    def __init__(self, base_directory: Optional[str] = None):
        if base_directory:
            self.base_dir = Path(base_directory)
        else:
            self.base_dir = Path.home() / "Pictures" / "RecordiaCaptures"
        
        self.screenshots_dir = self.base_dir / "Screenshots"
        self.recordings_dir = self.base_dir / "Recordings"
        self.ensure_directories()

    def set_base_directory(self, new_directory: str):
        """Update base storage directory and recreate paths."""
        self.base_dir = Path(new_directory)
        self.screenshots_dir = self.base_dir / "Screenshots"
        self.recordings_dir = self.base_dir / "Recordings"
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure storage folders exist on the filesystem."""
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.recordings_dir.mkdir(parents=True, exist_ok=True)

    def generate_screenshot_path(self, extension: str = "png") -> str:
        """Generate a unique timestamped file path for a screenshot."""
        self.ensure_directories()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ext = extension.lstrip(".")
        filename = f"screenshot_{timestamp}.{ext}"
        return str(self.screenshots_dir / filename)

    def generate_recording_path(self, extension: str = "mp4") -> str:
        """Generate a unique timestamped file path for a video recording."""
        self.ensure_directories()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ext = extension.lstrip(".")
        filename = f"recording_{timestamp}.{ext}"
        return str(self.recordings_dir / filename)

    def open_captures_folder(self):
        """Open the base capture folder in the system file explorer."""
        self.ensure_directories()
        target = str(self.base_dir)
        if sys.platform == "win32":
            os.startfile(target)
        elif sys.platform == "darwin":
            subprocess.run(["open", target])
        else:
            subprocess.run(["xdg-open", target])
