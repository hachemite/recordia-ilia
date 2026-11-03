"""
Settings configuration dialog for RecordiaILIA.
Allows configuring storage directory, formats, video FPS, and customizable hotkeys.
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
        self.window.geometry("480x380")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        # Variables
        self.save_dir_var = tk.StringVar(value=self.settings.get("save_directory", ""))
        self.format_var = tk.StringVar(value=self.settings.get("screenshot_format", "png"))
        self.fps_var = tk.IntVar(value=self.settings.get("video_fps", 30))
        
        current_hotkeys = self.settings.get("hotkeys", {})
        self.screenshot_hotkey_var = tk.StringVar(value=current_hotkeys.get("screenshot", "<ctrl>+<shift>+s"))
        self.record_hotkey_var = tk.StringVar(value=current_hotkeys.get("toggle_record", "<ctrl>+<shift>+r"))

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.window, padx=16, pady=16)
        frame.pack(fill=tk.BOTH, expand=True)

        # Storage directory section
        tk.Label(frame, text="Storage Directory:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 2))
        dir_frame = tk.Frame(frame)
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        entry = tk.Entry(dir_frame, textvariable=self.save_dir_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        tk.Button(dir_frame, text="Browse...", command=self._browse_dir).pack(side=tk.RIGHT)

        # Hotkeys configuration section (User choice)
        tk.Label(frame, text="Custom Capture Hotkeys:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 2))
        hotkey_box = tk.LabelFrame(frame, text=" Keyboard Shortcuts ", padx=8, pady=6)
        hotkey_box.pack(fill=tk.X, pady=(0, 10))

        hk_row1 = tk.Frame(hotkey_box)
        hk_row1.pack(fill=tk.X, pady=2)
        tk.Label(hk_row1, text="Step Capture Key:", width=18, anchor=tk.W).pack(side=tk.LEFT)
        tk.Entry(hk_row1, textvariable=self.screenshot_hotkey_var, width=22).pack(side=tk.LEFT)
        tk.Label(hk_row1, text=" (e.g. <f9> or <ctrl>+<shift>+s)", font=("Arial", 8), fg="gray").pack(side=tk.LEFT)

        hk_row2 = tk.Frame(hotkey_box)
        hk_row2.pack(fill=tk.X, pady=2)
        tk.Label(hk_row2, text="Video Recording Key:", width=18, anchor=tk.W).pack(side=tk.LEFT)
        tk.Entry(hk_row2, textvariable=self.record_hotkey_var, width=22).pack(side=tk.LEFT)
        tk.Label(hk_row2, text=" (e.g. <f10> or <ctrl>+<shift>+r)", font=("Arial", 8), fg="gray").pack(side=tk.LEFT)

        # Screenshot format section
        tk.Label(frame, text="Default Screenshot Format:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 2))
        format_frame = tk.Frame(frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Radiobutton(format_frame, text="PNG (Lossless)", variable=self.format_var, value="png").pack(side=tk.LEFT, padx=(0, 16))
        ttk.Radiobutton(format_frame, text="JPG (Compressed)", variable=self.format_var, value="jpg").pack(side=tk.LEFT)

        # Video FPS section
        tk.Label(frame, text="Screen Recording FPS:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(0, 2))
        fps_frame = tk.Frame(frame)
        fps_frame.pack(fill=tk.X, pady=(0, 14))
        fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_var, values=[15, 30, 60], state="readonly", width=10)
        fps_combo.pack(anchor=tk.W)

        # Action buttons
        btn_frame = tk.Frame(frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(btn_frame, text="Cancel", width=10, command=self.window.destroy).pack(side=tk.RIGHT, padx=(8, 0))
        tk.Button(btn_frame, text="Save", width=10, bg="#2563eb", fg="white", font=("Arial", 9, "bold"), command=self._save_settings).pack(side=tk.RIGHT)

    def _browse_dir(self):
        chosen = filedialog.askdirectory(initialdir=self.save_dir_var.get(), parent=self.window)
        if chosen:
            self.save_dir_var.set(chosen)

    def _save_settings(self):
        new_dir = self.save_dir_var.get().strip()
        if not new_dir:
            messagebox.showerror("Error", "Storage directory cannot be empty.", parent=self.window)
            return

        ss_hk = self.screenshot_hotkey_var.get().strip().lower()
        vid_hk = self.record_hotkey_var.get().strip().lower()

        if not ss_hk or not vid_hk:
            messagebox.showerror("Error", "Hotkey shortcuts cannot be empty.", parent=self.window)
            return

        self.settings.set("save_directory", new_dir)
        self.settings.set("screenshot_format", self.format_var.get())
        self.settings.set("video_fps", int(self.fps_var.get()))
        self.settings.set("hotkeys", {
            "screenshot": ss_hk,
            "toggle_record": vid_hk
        })

        if self.on_save:
            self.on_save()

        messagebox.showinfo("Saved", "Settings successfully saved!", parent=self.window)
        self.window.destroy()
