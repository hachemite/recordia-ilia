"""
Step annotation dialog for RecordiaILIA Steps Recorder.
Allows user to review detected app name and window title, and enter an optional description.
"""

import tkinter as tk
from typing import Optional, Dict, Any


class StepDialog:
    """Dialog allowing user to view detected window info and annotate a captured step."""

    def __init__(self, parent: tk.Tk, step_num: int, window_info: Dict[str, Any]):
        self.step_num = step_num
        self.window_info = window_info
        self.result: Optional[str] = None
        self.quick_mode: bool = False

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Annotate Step {step_num} - Recordia ILIA")
        self.dialog.geometry("440x260")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._build_ui()
        self.dialog.wait_window()

    def _build_ui(self):
        pad = tk.Frame(self.dialog, padx=16, pady=16)
        pad.pack(fill=tk.BOTH, expand=True)

        app_name = self.window_info.get("app_name", "Desktop")
        win_title = self.window_info.get("window_title", "Active Screen")

        tk.Label(pad, text=f"Step #{self.step_num} Captured", font=("Arial", 12, "bold"), fg="#2563eb").pack(anchor=tk.W)
        tk.Label(pad, text=f"Application: {app_name}", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(6, 2))
        tk.Label(pad, text=f"Window: {win_title}", font=("Arial", 8), fg="#555").pack(anchor=tk.W, pady=(0, 10))

        tk.Label(pad, text="Description / Action performed:", font=("Arial", 9)).pack(anchor=tk.W)
        self.desc_entry = tk.Entry(pad, font=("Arial", 10), width=45)
        self.desc_entry.insert(0, f"Performed action on {app_name}")
        self.desc_entry.pack(fill=tk.X, pady=(4, 10))
        self.desc_entry.focus_set()
        self.desc_entry.select_range(0, tk.END)

        self.quick_var = tk.BooleanVar(value=False)
        tk.Checkbutton(pad, text="Quick Mode (Auto-save steps without asking for this session)", variable=self.quick_var).pack(anchor=tk.W, pady=(0, 12))

        btn_row = tk.Frame(pad)
        btn_row.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(btn_row, text="Cancel", width=10, command=self._on_cancel).pack(side=tk.RIGHT, padx=(6, 0))
        tk.Button(btn_row, text="Save Step", width=12, bg="#2563eb", fg="white", font=("Arial", 9, "bold"), command=self._on_save).pack(side=tk.RIGHT)

        self.dialog.bind("<Return>", lambda e: self._on_save())
        self.dialog.bind("<Escape>", lambda e: self._on_cancel())

    def _on_save(self):
        self.result = self.desc_entry.get().strip()
        self.quick_mode = self.quick_var.get()
        self.dialog.destroy()

    def _on_cancel(self):
        self.result = None
        self.dialog.destroy()
