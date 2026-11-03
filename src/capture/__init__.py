"""Capture module providing screenshot and screen recording engines."""
from .base import BaseScreenshotEngine, BaseRecordingEngine
from .screenshot import ScreenshotEngine
from .recorder import ScreenRecorder

__all__ = ["BaseScreenshotEngine", "BaseRecordingEngine", "ScreenshotEngine", "ScreenRecorder"]
