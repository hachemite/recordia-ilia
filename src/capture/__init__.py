"""Capture module providing screenshot and screen recording engines."""
from .base import BaseScreenshotEngine, BaseRecordingEngine
from .screenshot import ScreenshotEngine

__all__ = ["BaseScreenshotEngine", "BaseRecordingEngine", "ScreenshotEngine"]
