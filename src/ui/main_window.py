"""
Desktop User Interface for RecordiaILIA Steps Recorder.
"""

import tkinter as tk
from tkinter import messagebox


class MainWindow:
    def __init__(
        self,
        on_record_step=None,
        on_finish_session=None,
        on_screenshot=None,
        on_start_record=None,
        on_stop_record=None,
        on_open_settings=None,
        on_open_captures=None,
        on_close=None
    ):
        self.on_record_step = on_record_step or on_screenshot or (lambda: print("record step"))
        self.on_finish_session = on_finish_session or (lambda: print("finish session"))
        self.on_screenshot = on_screenshot or self.on_record_step
        self.on_start_record = on_start_record or (lambda: print("start recording"))
        self.on_stop_record = on_stop_record or (lambda: print("stop recording"))
        self.on_open_settings = on_open_settings or (lambda: print("settings"))
        self.on_open_captures = on_open_captures or (lambda: print("captures folder"))
        self.on_close = on_close

        self.root = tk.Tk()
        self.root.title("Recordia ILIA - Steps Recorder")
        self.root.geometry("440x440")
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

        self.status = tk.StringVar(value="Ready to record steps")
        self.step_counter_var = tk.StringVar(value="Steps in session: 0")
        self.project_name_var = tk.StringVar(value="My_Project")

        self._build_ui()

    def _build_ui(self):
        # Header
        tk.Label(self.root, text="Recordia ILIA", font=("Arial", 16, "bold"), fg="#1e293b").pack(pady=(12, 2))
        tk.Label(self.root, text="Automated Step & Screen Recorder", font=("Arial", 9), fg="#64748b").pack(pady=(0, 10))

        # Project Session Section
        proj_frame = tk.LabelFrame(self.root, text=" Active Project / Session ", font=("Arial", 9, "bold"), padx=10, pady=8)
        proj_frame.pack(fill=tk.X, padx=16, pady=(0, 10))

        name_row = tk.Frame(proj_frame)
        name_row.pack(fill=tk.X)
        tk.Label(name_row, text="Project Name:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 6))
        tk.Entry(name_row, textvariable=self.project_name_var, font=("Arial", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        counter_lbl = tk.Label(proj_frame, textvariable=self.step_counter_var, font=("Arial", 9, "bold"), fg="#2563eb")
        counter_lbl.pack(anchor=tk.W, pady=(6, 0))

        # Step Actions
        tk.Button(
            self.root,
            text="📸 Capture Step (Ctrl+Shift+S)",
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            height=2,
            width=32,
            command=self._record_step
        ).pack(pady=4)

        tk.Button(
            self.root,
            text="📄 Finish & Export HTML Report",
            bg="#059669",
            fg="white",
            font=("Arial", 10, "bold"),
            width=32,
            command=self._finish_session
        ).pack(pady=4)

        # Video recording section
        vid_frame = tk.Frame(self.root)
        vid_frame.pack(pady=4)
        tk.Button(vid_frame, text="Start Video 🎥", width=15, command=self._start_video).pack(side=tk.LEFT, padx=3)
        tk.Button(vid_frame, text="Stop Video ⏹️", width=15, command=self._stop_video).pack(side=tk.LEFT, padx=3)

        # Secondary utilities
        util_frame = tk.Frame(self.root)
        util_frame.pack(pady=4)
        tk.Button(util_frame, text="Open Captures 📁", width=15, command=self.on_open_captures).pack(side=tk.LEFT, padx=3)
        tk.Button(util_frame, text="Settings ⚙️", width=15, command=self.on_open_settings).pack(side=tk.LEFT, padx=3)

        # Status text
        self.status_label = tk.Label(self.root, textvariable=self.status, font=("Arial", 9, "italic"), fg="#334155")
        self.status_label.pack(pady=6)

        # Hotkey legend footer
        tk.Label(
            self.root,
            text="Global Hotkeys: Step Capture [Ctrl+Shift+S] | Video [Ctrl+Shift+R]",
            font=("Arial", 8),
            fg="gray"
        ).pack(side=tk.BOTTOM, pady=8)

    def set_status(self, text: str):
        """Thread-safe status text updater."""
        self.root.after(0, lambda: self.status.set(text))

    def update_step_count(self, count: int):
        """Thread-safe step counter updater."""
        self.root.after(0, lambda: self.step_counter_var.set(f"Steps in session: {count}"))

    def get_project_name(self) -> str:
        return self.project_name_var.get().strip() or "Project"

    def _record_step(self):
        self.on_record_step()

    def _finish_session(self):
        self.on_finish_session()

    def _start_video(self):
        self.on_start_record()
        self.set_status("Video recording in progress...")

    def _stop_video(self):
        self.on_stop_record()
        self.set_status("Video recording stopped")

    def _on_window_close(self):
        if self.on_close:
            self.on_close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
