"""
Screen recording engine for RecordiaILIA.
Captures screen frames continuously and encodes them into a video file in a background thread.
"""

import os
import threading
import time
from typing import Optional
import cv2
import numpy as np
import mss

from capture.base import BaseRecordingEngine
from storage.file_manager import FileManager


class ScreenRecorder(BaseRecordingEngine):
    """Engine responsible for capturing desktop frames and encoding video."""

    def __init__(self, file_manager: FileManager, fps: int = 30, video_format: str = "mp4"):
        self.file_manager = file_manager
        self.fps = fps
        self.video_format = video_format

        self._is_recording = False
        self._thread: Optional[threading.Thread] = None
        self._current_filepath: Optional[str] = None
        self._lock = threading.Lock()
        self._thread_error: Optional[str] = None

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    def start_recording(self, save_path: Optional[str] = None) -> str:
        """
        Starts video capture in a separate worker thread.
        """
        with self._lock:
            if self._is_recording:
                return self._current_filepath or ""

            ext = self.video_format.lstrip(".")
            self._current_filepath = save_path or self.file_manager.generate_recording_path(ext)
            self._is_recording = True
            self._thread_error = None

            self._thread = threading.Thread(
                target=self._record_loop,
                args=(self._current_filepath,),
                daemon=True
            )
            self._thread.start()
            return self._current_filepath

    def stop_recording(self) -> str:
        """
        Stops the recording loop and finalizes the output video.
        Waits for the worker thread to finish; raises RuntimeError if the
        thread could not be stopped or failed during recording.
        Returns the saved file path.
        """
        with self._lock:
            if not self._is_recording:
                return self._current_filepath or ""
            self._is_recording = False

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=10.0)
            if self._thread.is_alive():
                raise RuntimeError("Recorder thread did not terminate after stop_recording().")

        thread_error = self._thread_error
        saved_path = self._current_filepath or ""
        self._current_filepath = None
        if thread_error:
            raise RuntimeError(f"Recording failed: {thread_error}")

        return saved_path

    def _record_loop(self, output_path: str):
        """Worker thread loop capturing and writing frames."""
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        frame_interval = 1.0 / max(1, self.fps)

        try:
            # Determine screen dimensions
            try:
                with mss.MSS() as sct:
                    monitor = sct.monitors[0]
                    width = monitor["width"]
                    height = monitor["height"]
            except Exception as exc:
                raise RuntimeError(f"Could not determine screen dimensions via mss: {exc}")

            # Ensure width and height are even numbers (required by many video encoders)
            width = width if width % 2 == 0 else width - 1
            height = height if height % 2 == 0 else height - 1

            writer = cv2.VideoWriter(output_path, fourcc, float(self.fps), (width, height))
            if not writer.isOpened():
                raise RuntimeError(
                    f"cv2.VideoWriter could not open '{output_path}' "
                    f"(codec 'mp4v', {width}x{height} @ {self.fps} fps)."
                )

            frame_count = 0
            with mss.MSS() as sct:
                monitor = sct.monitors[0]
                while self._is_recording:
                    t_start = time.time()

                    try:
                        sct_img = sct.grab(monitor)
                        frame = np.array(sct_img)
                        # Convert BGRA to BGR
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                        if frame_bgr.shape[1] != width or frame_bgr.shape[0] != height:
                            frame_bgr = cv2.resize(frame_bgr, (width, height))
                    except Exception as exc:
                        raise RuntimeError(f"Frame capture failed at frame {frame_count}: {exc}")

                    writer.write(frame_bgr)
                    frame_count += 1

                    elapsed = time.time() - t_start
                    sleep_time = frame_interval - elapsed
                    if sleep_time > 0:
                        time.sleep(sleep_time)
        except Exception as exc:
            self._thread_error = str(exc)
        finally:
            writer = locals().get("writer")
            if writer is not None:
                writer.release()
