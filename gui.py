"""
This program is a simple transcriber, that transcribes 
audio files and returns an SRT-file. The transcribing is
done by OpenAI's Whisper model: https://github.com/openai/whisper

This code bundles into an .exe-file that runs on Windows. It is developed on a Windows 11 machine, 
but has run succesfully on Windows 7 and 10 machines.

Author: Martin Dreyer
"""

# This file is part of T-tex.
#
# T-tex is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 3, as published by
# the Free Software Foundation.
#
# T-tex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with T-tex. If not, see <https://www.gnu.org/licenses/>.


import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import helper_functions as helper_functions
import threading
import os
import subprocess
import sys


def is_ffmpeg_available():
    try:
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")
        subprocess.run([ffmpeg_path, "-version"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    


class Redirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        # Append the text to the Text widget
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)

class TranscriberApp(tk.Tk):
    def __init__(self):
        FONT = 'Helvetica'
        COLOR = "#102542"
        BACKGROUND = '#CDD7D6'
        BUTTON_COLOR = '#FFFFFF'
        BUTTON_BG = "#102542"
        HEIGHT = 200
        WIDTH = 750
        TEXTBOX_BACKGROUND = "#FFFFFF"
        TEXTBOX_COLOR = "#102542"

        super().__init__()
        self.frame = tk.Frame(self, height=HEIGHT, width=WIDTH)
        self.frame.config(bg=BACKGROUND, )
        self.config(bg=BACKGROUND)
        self.title("windowshvisker")
        self.frame.grid()

        self.label = tk.Label(
            self, text="Vælg en fil for at få den transskriberet", 
            bg=BACKGROUND,
            fg=COLOR,
            font=(FONT, 18, 'bold')
        )
        self.label.grid(column=0, row=0)

        self.button = tk.Button(
            self, 
            text="Vælg Fil", 
            bg=BUTTON_BG, 
            fg=BUTTON_COLOR, 
            relief= 'raised', 
            font=(FONT, 14, 'bold'),
            borderwidth=2, 
            command=self.handle_upload)
        
        self.button.grid(column=0, row=1, pady=(HEIGHT/10))

        self.textbox = tk.Text(
            self, 
            wrap=tk.WORD, 
            bg=TEXTBOX_BACKGROUND,
            fg=TEXTBOX_COLOR, 
            borderwidth=0,
            padx=10,
            pady=10,
            font=(FONT, 12)
            )
        self.textbox.grid(column=0, row=2, pady=40, padx=40)
        sys.stdout = Redirector(self.textbox)
    
    def handle_upload(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Disable the button to avoid multiple clicks during transcription
            self.button.config(state=tk.DISABLED)

            # Start the transcription task in a separate thread
            transcription_thread = threading.Thread(
                target=self.transcribe_and_save_srt, args=(file_path,)
            )
            transcription_thread.start()

    def transcribe_and_save_srt(self, file_path):
        try:
            transcription = helper_functions.transcribe(helper_functions.get_resource_path(file_path))
            srt_file = helper_functions.get_srt_name(helper_functions.get_resource_path(file_path))
            if transcription:
                # Ask the user to specify the save location
                save_path = filedialog.asksaveasfilename(
                    title="Gem fil som",
                    defaultextension=".srt",
                    filetype=[("SubRip (.srt)", ".srt")],
                    initialfile=srt_file,
                )
                if save_path:
                    # Save the content directly to the user-specified location
                    helper_functions.output_to_text_file(
                        transcription, helper_functions.get_resource_path(save_path)
                    )
                    # Show a success message to the user
                    messagebox.showinfo("Fil Gemt", "Din SRT-fil er gemt!")

        except Exception as e:
            # Show an error message to the user if something goes wrong
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Re-enable the button after transcription is done or if an error occurred
            self.button.config(state=tk.NORMAL)


def main():
    helper_functions.set_ffmpeg_path()
    print("Loading")

    if is_ffmpeg_available():
        print("ffmpeg is available!")
    else:
        print("ffmpeg is not available!")

    app = TranscriberApp()
    app.mainloop()


if __name__ == "__main__":
    main()
