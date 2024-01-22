import tkinter as tk
from io import StringIO
import sys

class Redirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = StringIO()

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout

    def write(self, text):
        self.buffer.write(text)
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)  # Scroll to the end of the Text widget

    def flush(self):
        pass