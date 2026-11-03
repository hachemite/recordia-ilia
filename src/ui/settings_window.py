"""
Settings configuration dialog for RecordiaILIA.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable, Optional
from config.settings import Settings


class SettingsWindow:
    """Toplevel modal window for editing user preferences."""

    def __init__(self, parent: tk.Tk, settings: Settings, on_save: Optional[Callable] = None):
        self.settings = settings
        self.on_save = on_save

        self.window = tk.Toplevel(parent)
        self.window.title("Settings - Recordia ILIA")
        self.window.geometry("450x300")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        # Variables
        self.save_dir_var = tk.StringVar(value=self.settings.get("save_directory", ""))
        self.format_var = tk.StringVar(value=self.settings.get("screenshot_format", "png"))
        self.fps_var = tk.IntVar(value=self.settings.get("video_fps", 30))

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.window, padx=16, pady=16)
        frame.pack(fill=tk.BOTH, expand=True)

        # Storage directory section
        tk.Label(frame, text="Storage Directory:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 2))
        dir_frame = tk.Frame(frame)
        dir_frame.pack(fill=tk.X, pady=(0, 12))
        
        entry = tk.Entry(dir_frame, textvariable=self.save_dir_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        tk.Button(dir_frame, text="Browse...", command=self._browse_dir).pack(side=tk.RIGHT)

        # Screenshot format section
        tk.Label(frame, text="Default Screenshot Format:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 2))
        format_frame = tk.Frame(frame)
        format_frame.pack(fill=tk.X, pady=(0, 12))
        ttk.Radiobutton(format_frame, text="PNG (Lossless)", variable=self.format_var, value="png").pack(side=tk.LEFT, padx=(0, 16))
        ttk.Radiobutton(format_frame, text="JPG (Compressed)", variable=self.format_var, value="jpg").pack(side=tk.LEFT)

        # Video FPS section
        tk.Label(frame, text="Screen Recording FPS:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 2))
        fps_frame = tk.Frame(frame)
        fps_frame.pack(fill=tk.X, pady=(0, 16))
        fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_var, values=[15, 30, 60], state="readonly", width=10)
        fps_combo.pack(anchor=tk.W)

        # Action buttons
        btn_frame = tk.Frame(frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(btn_frame, text="Cancel", width=10, command=self.window.destroy).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(btn_frame, text="Save", width=10, bg="#4CAF50", fg="white", command=self._save_settings).pack(side=tk.RIGHT)

    def _browse_dir(self):
        chosen = filedialog.askdirectory(initialdir=self.save_dir_var.get(), parent=self.window)
        if chosen:
            self.save_dir_var.set(chosen)

    def _save_settings(self):
        new_dir = self.save_dir_var.get().strip()
        if not new_dir:
            messagebox.showerror("Error", "Storage directory cannot be empty.", parent=self.window)
            return

        self.settings.set("save_directory", new_dir)
        self.settings.set("screenshot_format", self.format_var.get())
        self.settings.set("video_fps", int(self.fps_var.get()))

        if self.on_save:
            self.on_save()

        messagebox.showinfo("Saved", "Settings successfully saved!", parent=self.window)
        self.window.destroy()
