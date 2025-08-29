import tkinter as tk
from tkinter import font
from datetime import datetime
import time
import sys
import os

# Function to locate resources inside PyInstaller bundle
def resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TapClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Tap Clock")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Set .ico icon for title bar and taskbar
        ico_path = resource_path("clock.ico")
        try:
            self.root.iconbitmap(ico_path)
        except:
            print("Icon not found, using default")

        # Allow maximize/minimize/resize
        self.root.minsize(300, 200)

        # Modes
        self.is_clock = True
        self.stopwatch_running = False
        self.stopwatch_start = 0
        self.stopwatch_elapsed = 0

        # Base font
        self.font_family = "Helvetica"
        self.font_size = 80
        self.clock_font = font.Font(family=self.font_family, size=self.font_size, weight="bold")

        # Clock label
        self.label = tk.Label(root, text="", font=self.clock_font, fg="white", bg="black")
        self.label.pack(expand=True, fill="both")

        # Bind resize → dynamic font scaling
        self.root.bind("<Configure>", self.resize_font)

        # Fullscreen toggle (F11)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.fullscreen = False

        # Tap bindings
        self.root.bind("<Button-1>", self.single_tap)
        self.root.bind("<Double-1>", self.double_tap)
        self.root.bind("<Triple-1>", self.triple_tap)
        self.root.bind("<Button-3>", self.quadruple_tap)

        self.update_clock()

    def resize_font(self, event=None):
        new_size = min(self.root.winfo_width() // 6, self.root.winfo_height() // 2)
        self.clock_font.configure(size=max(20, new_size))

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def update_clock(self):
        if self.is_clock:
            now = datetime.now().strftime("%H:%M:%S")
            self.label.config(text=now)
        else:
            if self.stopwatch_running:
                elapsed = time.time() - self.stopwatch_start + self.stopwatch_elapsed
            else:
                elapsed = self.stopwatch_elapsed
            mins, secs = divmod(int(elapsed), 60)
            self.label.config(text=f"{mins:02}:{secs:02}")
        self.root.after(100, self.update_clock)

    # Tap actions
    def single_tap(self, event):
        if not self.is_clock:
            if not self.stopwatch_running:
                self.stopwatch_running = True
                self.stopwatch_start = time.time()
            else:
                self.stopwatch_running = False
                self.stopwatch_elapsed += time.time() - self.stopwatch_start

    def double_tap(self, event):
        if not self.is_clock:
            self.stopwatch_running = False
            self.stopwatch_elapsed = 0

    def triple_tap(self, event):
        self.is_clock = not self.is_clock
        if self.is_clock:
            self.stopwatch_running = False
            self.stopwatch_elapsed = 0

    def quadruple_tap(self, event):
        if not self.is_clock:
            self.stopwatch_running = False
            self.stopwatch_elapsed = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = TapClock(root)
    root.mainloop()
