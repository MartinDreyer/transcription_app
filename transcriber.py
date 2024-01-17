import tkinter as tk
from tkinter import StringVar
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import threading
from settings import *

class Transcriber:
    def __init__(self, button, textbox):
        self.button = button
        self.textbox = textbox
        self.MODEL_SIZE = MODEL_SIZE

    def handle_upload(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.button.config(state=tk.DISABLED)
            transcription_thread = threading.Thread(
                target=self.transcribe, args=(file_path,)
            )
            transcription_thread.start()

    def transcribe(self, file_path):
        try:
            print(f'Transcribing {file_path.split("/")[-1]} using {self.MODEL_SIZE} model')
            # Transcribe file using correct model size
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
        finally:
            self.button.config(state=tk.NORMAL)
