import tkinter as tk
from tkinter import messagebox


class MainWindow:
    def __init__(self, on_screenshot=None, on_start_record=None, on_stop_record=None, on_close=None):
        # Callbacks are filled by the capture module (Hachem's part)
        self.on_screenshot = on_screenshot or (lambda: print("screenshot (not implemented yet)"))
        self.on_start_record = on_start_record or (lambda: print("start recording (not implemented yet)"))
        self.on_stop_record = on_stop_record or (lambda: print("stop recording (not implemented yet)"))
        self.on_close = on_close

        self.root = tk.Tk()
        self.root.title("Recordia ILIA")
        self.root.geometry("380x280")
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

        self.status = tk.StringVar(value="Ready")

        tk.Label(self.root, text="Recordia ILIA", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(self.root, text="Take screenshot (Ctrl+Shift+S)", width=28, command=self._screenshot).pack(pady=4)
        tk.Button(self.root, text="Start recording (Ctrl+Shift+R)", width=28, command=self._start).pack(pady=4)
        tk.Button(self.root, text="Stop recording", width=28, command=self._stop).pack(pady=4)
        
        self.status_label = tk.Label(self.root, textvariable=self.status, font=("Arial", 10, "italic"))
        self.status_label.pack(pady=8)

        tk.Label(
            self.root,
            text="Global Hotkeys:\nScreenshot: Ctrl+Shift+S | Record: Ctrl+Shift+R",
            font=("Arial", 8),
            fg="gray"
        ).pack(side=tk.BOTTOM, pady=6)

    def set_status(self, text: str):
        """Thread-safe status text updater."""
        self.root.after(0, lambda: self.status.set(text))

    def _screenshot(self):
        self.on_screenshot()
        self.set_status("Screenshot taken")

    def _start(self):
        self.on_start_record()
        self.set_status("Recording...")

    def _stop(self):
        self.on_stop_record()
        self.set_status("Recording stopped")

    def _on_window_close(self):
        if self.on_close:
            self.on_close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
