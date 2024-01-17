import tkinter as tk


class Redirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        # Append the text to the Text widget
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
