"""
Step editor and review window for RecordiaILIA.
Allows users to review captured steps, inspect details, and update descriptions
either during an active session or before exporting reports.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from storage.session_manager import SessionManager, StepRecord


class StepEditorWindow:
    """Toplevel window for reviewing and editing step descriptions."""

    def __init__(self, parent: tk.Tk, session_manager: SessionManager, on_updated: Optional[Callable] = None):
        self.session_manager = session_manager
        self.on_updated = on_updated

        self.window = tk.Toplevel(parent)
        self.window.title("Review & Edit Steps - Recordia ILIA")
        self.window.geometry("640x440")
        self.window.minsize(540, 360)
        self.window.transient(parent)

        self.selected_step: Optional[StepRecord] = None
        self._build_ui()
        self._populate_steps()

    def _build_ui(self):
        container = tk.Frame(self.window, padx=12, pady=12)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            container,
            text="Session Steps Review",
            font=("Arial", 12, "bold"),
            fg="#1e293b"
        ).pack(anchor=tk.W, pady=(0, 4))
        tk.Label(
            container,
            text="Select any step from the list below to review or update its description.",
            font=("Arial", 9),
            fg="#64748b"
        ).pack(anchor=tk.W, pady=(0, 10))

        # Split pane: List on top, editor on bottom
        tree_frame = tk.Frame(container)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        columns = ("step", "time", "app", "desc")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        self.tree.heading("step", text="Step #")
        self.tree.heading("time", text="Timestamp")
        self.tree.heading("app", text="Application")
        self.tree.heading("desc", text="Description")

        self.tree.column("step", width=60, anchor=tk.CENTER)
        self.tree.column("time", width=140, anchor=tk.CENTER)
        self.tree.column("app", width=120, anchor=tk.W)
        self.tree.column("desc", width=260, anchor=tk.W)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_step_selected)

        # Editor Panel
        edit_box = tk.LabelFrame(container, text=" Edit Description ", font=("Arial", 9, "bold"), padx=10, pady=8)
        edit_box.pack(fill=tk.X, pady=(0, 10))

        self.info_label = tk.Label(edit_box, text="Select a step above to edit.", font=("Arial", 9, "italic"), fg="#555")
        self.info_label.pack(anchor=tk.W, pady=(0, 4))

        self.desc_text = tk.Text(edit_box, height=3, font=("Arial", 9))
        self.desc_text.pack(fill=tk.X, pady=(0, 6))

        btn_row = tk.Frame(edit_box)
        btn_row.pack(fill=tk.X)
        self.save_btn = tk.Button(
            btn_row,
            text="Save Description",
            bg="#2563eb",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self._save_description,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT)

        self.feedback_label = tk.Label(btn_row, text="", font=("Arial", 9), fg="#16a34a")
        self.feedback_label.pack(side=tk.LEFT, padx=10)

        # Footer
        tk.Button(container, text="Close", width=10, command=self.window.destroy).pack(side=tk.RIGHT)

    def _populate_steps(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        steps = self.session_manager.get_steps()
        for s in steps:
            self.tree.insert("", tk.END, iid=str(s.step_number), values=(
                f"Step {s.step_number}",
                s.timestamp,
                s.app_name,
                s.description
            ))

    def _on_step_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        step_num = int(selected[0])
        steps = self.session_manager.get_steps()
        matching = [s for s in steps if s.step_number == step_num]
        if not matching:
            return

        self.selected_step = matching[0]
        self.info_label.config(
            text=f"Step #{self.selected_step.step_number} | Application: {self.selected_step.app_name} | Window: {self.selected_step.window_title}",
            font=("Arial", 9)
        )
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", self.selected_step.description)
        self.save_btn.config(state=tk.NORMAL)
        self.feedback_label.config(text="")

    def _save_description(self):
        if not self.selected_step:
            return

        new_desc = self.desc_text.get("1.0", tk.END).strip()
        updated = self.session_manager.update_step_description(self.selected_step.step_number, new_desc)
        if updated:
            self.feedback_label.config(text="Description saved successfully!")
            self._populate_steps()
            self.tree.selection_set(str(self.selected_step.step_number))
            if self.on_updated:
                self.on_updated()
