"""
Base abstractions for screen capture and recording engines.
"""

from abc import ABC, abstractmethod


class BaseScreenshotEngine(ABC):
    """Interface for screenshot capture implementations."""

    @abstractmethod
    def capture_fullscreen(self) -> str:
        """Capture the full screen and return the saved filepath."""
        pass


class BaseRecordingEngine(ABC):
    """Interface for screen recording implementations."""

    @abstractmethod
    def start_recording(self):
        """Start recording screen frames."""
        pass

    @abstractmethod
    def stop_recording(self) -> str:
        """Stop recording and return the saved video filepath."""
        pass

    @property
    @abstractmethod
    def is_recording(self) -> bool:
        """Returns True if recording is currently active."""
        pass
