import tkinter as tk
from tkinter import messagebox


class MainWindow:
    def __init__(self, on_screenshot=None, on_start_record=None, on_stop_record=None):
        # Callbacks are filled by the capture module (Hachem's part)
        self.on_screenshot = on_screenshot or (lambda: print("screenshot (not implemented yet)"))
        self.on_start_record = on_start_record or (lambda: print("start recording (not implemented yet)"))
        self.on_stop_record = on_stop_record or (lambda: print("stop recording (not implemented yet)"))

        self.root = tk.Tk()
        self.root.title("Recordia ILIA")
        self.root.geometry("360x240")

        self.status = tk.StringVar(value="Ready")

        tk.Label(self.root, text="Recordia ILIA", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(self.root, text="Take screenshot", width=24, command=self._screenshot).pack(pady=4)
        tk.Button(self.root, text="Start recording", width=24, command=self._start).pack(pady=4)
        tk.Button(self.root, text="Stop recording", width=24, command=self._stop).pack(pady=4)
        tk.Label(self.root, textvariable=self.status).pack(pady=10)

    def _screenshot(self):
        self.on_screenshot()
        self.status.set("Screenshot taken")

    def _start(self):
        self.on_start_record()
        self.status.set("Recording...")

    def _stop(self):
        self.on_stop_record()
        self.status.set("Recording stopped")

    def run(self):
        self.root.mainloop()