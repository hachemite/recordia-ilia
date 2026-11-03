"""
Desktop User Interface for RecordiaILIA Steps Recorder.
Supports Manual, On-Click, and Periodic Interval auto-capture modes.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class MainWindow:
    def __init__(
        self,
        on_record_step=None,
        on_finish_session=None,
        on_toggle_auto=None,
        on_screenshot=None,
        on_start_record=None,
        on_stop_record=None,
        on_open_settings=None,
        on_open_captures=None,
        on_close=None
    ):
        self.on_record_step = on_record_step or on_screenshot or (lambda: print("record step"))
        self.on_finish_session = on_finish_session or (lambda: print("finish session"))
        self.on_toggle_auto = on_toggle_auto or (lambda mode, interval: print(f"toggle auto: {mode}, {interval}"))
        self.on_screenshot = on_screenshot or self.on_record_step
        self.on_start_record = on_start_record or (lambda: print("start recording"))
        self.on_stop_record = on_stop_record or (lambda: print("stop recording"))
        self.on_open_settings = on_open_settings or (lambda: print("settings"))
        self.on_open_captures = on_open_captures or (lambda: print("captures folder"))
        self.on_close = on_close

        self.root = tk.Tk()
        self.root.title("Recordia ILIA - Steps Recorder")
        self.root.geometry("460x520")
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

        self.status = tk.StringVar(value="Ready to record steps")
        self.step_counter_var = tk.StringVar(value="Steps in session: 0")
        self.project_name_var = tk.StringVar(value="My_Project")
        self.trigger_mode_var = tk.StringVar(value="manual")
        self.interval_var = tk.DoubleVar(value=2.0)
        self.is_auto_running = False

        self._build_ui()

    def _build_ui(self):
        # Header
        tk.Label(self.root, text="Recordia ILIA", font=("Arial", 16, "bold"), fg="#1e293b").pack(pady=(10, 2))
        tk.Label(self.root, text="Automated Step & Screen Recorder", font=("Arial", 9), fg="#64748b").pack(pady=(0, 8))

        # Project Session Section
        proj_frame = tk.LabelFrame(self.root, text=" Active Project / Session ", font=("Arial", 9, "bold"), padx=10, pady=6)
        proj_frame.pack(fill=tk.X, padx=16, pady=(0, 8))

        name_row = tk.Frame(proj_frame)
        name_row.pack(fill=tk.X)
        tk.Label(name_row, text="Project Name:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 6))
        tk.Entry(name_row, textvariable=self.project_name_var, font=("Arial", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        counter_lbl = tk.Label(proj_frame, textvariable=self.step_counter_var, font=("Arial", 9, "bold"), fg="#2563eb")
        counter_lbl.pack(anchor=tk.W, pady=(4, 0))

        # Capture Mode Section
        mode_frame = tk.LabelFrame(self.root, text=" Step Trigger Mode (User's Choice) ", font=("Arial", 9, "bold"), padx=10, pady=6)
        mode_frame.pack(fill=tk.X, padx=16, pady=(0, 8))

        ttk.Radiobutton(
            mode_frame,
            text="Manual (Button / Ctrl+Shift+S)",
            variable=self.trigger_mode_var,
            value="manual",
            command=self._on_mode_change
        ).pack(anchor=tk.W, pady=1)

        ttk.Radiobutton(
            mode_frame,
            text="⚡ Auto on Mouse Click (Records every click)",
            variable=self.trigger_mode_var,
            value="on_click",
            command=self._on_mode_change
        ).pack(anchor=tk.W, pady=1)

        periodic_row = tk.Frame(mode_frame)
        periodic_row.pack(fill=tk.X, pady=1)
        ttk.Radiobutton(
            periodic_row,
            text="⏱️ Auto Periodic Timer:",
            variable=self.trigger_mode_var,
            value="periodic",
            command=self._on_mode_change
        ).pack(side=tk.LEFT)
        
        tk.Label(periodic_row, text=" Every", font=("Arial", 9)).pack(side=tk.LEFT, padx=(6, 2))
        tk.Spinbox(periodic_row, from_=0.5, to=60.0, increment=0.5, textvariable=self.interval_var, width=5).pack(side=tk.LEFT)
        tk.Label(periodic_row, text="sec", font=("Arial", 9)).pack(side=tk.LEFT, padx=(2, 0))

        # Dynamic Action Button (Changes based on mode)
        self.action_btn = tk.Button(
            self.root,
            text="📸 Capture Step (Ctrl+Shift+S)",
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            height=2,
            width=34,
            command=self._handle_primary_action
        )
        self.action_btn.pack(pady=4)

        tk.Button(
            self.root,
            text="📄 Finish & Export HTML Report",
            bg="#059669",
            fg="white",
            font=("Arial", 10, "bold"),
            width=34,
            command=self._finish_session
        ).pack(pady=3)

        # Video recording section
        vid_frame = tk.Frame(self.root)
        vid_frame.pack(pady=3)
        tk.Button(vid_frame, text="Start Video 🎥", width=16, command=self._start_video).pack(side=tk.LEFT, padx=3)
        tk.Button(vid_frame, text="Stop Video ⏹️", width=16, command=self._stop_video).pack(side=tk.LEFT, padx=3)

        # Secondary utilities
        util_frame = tk.Frame(self.root)
        util_frame.pack(pady=3)
        tk.Button(util_frame, text="Open Captures 📁", width=16, command=self.on_open_captures).pack(side=tk.LEFT, padx=3)
        tk.Button(util_frame, text="Settings ⚙️", width=16, command=self.on_open_settings).pack(side=tk.LEFT, padx=3)

        # Status text
        self.status_label = tk.Label(self.root, textvariable=self.status, font=("Arial", 9, "italic"), fg="#334155")
        self.status_label.pack(pady=4)

        # Hotkey legend footer
        tk.Label(
            self.root,
            text="Global Hotkeys: Step Capture [Ctrl+Shift+S] | Video [Ctrl+Shift+R]",
            font=("Arial", 8),
            fg="gray"
        ).pack(side=tk.BOTTOM, pady=6)

    def _on_mode_change(self):
        mode = self.trigger_mode_var.get()
        if self.is_auto_running:
            self._stop_auto_running()

        if mode == "manual":
            self.action_btn.config(
                text="📸 Capture Step (Ctrl+Shift+S)",
                bg="#2563eb"
            )
        else:
            self.action_btn.config(
                text=f"▶️ Start Auto-Recording ({'Click' if mode == 'on_click' else 'Timer'})",
                bg="#16a34a"
            )

    def _handle_primary_action(self):
        mode = self.trigger_mode_var.get()
        if mode == "manual":
            self.on_record_step()
        else:
            if not self.is_auto_running:
                self._start_auto_running()
            else:
                self._stop_auto_running()

    def _start_auto_running(self):
        mode = self.trigger_mode_var.get()
        try:
            interval = float(self.interval_var.get())
        except ValueError:
            interval = 2.0
            self.interval_var.set(2.0)

        self.is_auto_running = True
        self.action_btn.config(
            text=f"⏹️ Stop Auto-Recording ({'Click' if mode == 'on_click' else 'Timer'})",
            bg="#dc2626"
        )
        self.on_toggle_auto(mode, interval)

    def _stop_auto_running(self):
        self.is_auto_running = False
        mode = self.trigger_mode_var.get()
        self.action_btn.config(
            text=f"▶️ Start Auto-Recording ({'Click' if mode == 'on_click' else 'Timer'})",
            bg="#16a34a"
        )
        self.on_toggle_auto("stop", 0)

    def set_status(self, text: str):
        """Thread-safe status text updater."""
        self.root.after(0, lambda: self.status.set(text))

    def update_step_count(self, count: int):
        """Thread-safe step counter updater."""
        self.root.after(0, lambda: self.step_counter_var.set(f"Steps in session: {count}"))

    def get_project_name(self) -> str:
        return self.project_name_var.get().strip() or "Project"

    def _finish_session(self):
        if self.is_auto_running:
            self._stop_auto_running()
        self.on_finish_session()

    def _start_video(self):
        self.on_start_record()
        self.set_status("Video recording in progress...")

    def _stop_video(self):
        self.on_stop_record()
        self.set_status("Video recording stopped")

    def _on_window_close(self):
        if self.is_auto_running:
            self._stop_auto_running()
        if self.on_close:
            self.on_close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
