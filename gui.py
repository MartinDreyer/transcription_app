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
import threading
import os
import subprocess
import sys
import whisper
import traceback
import re

# Transcriber settings
MODEL_SIZE = "large"
LANGUAGE = "danish"
ALLOWED_EXTENSIONS = ["wav", "mp3", "mp4", "mpga", "webm", "m4a"]

# GUI Styling
FONT = 'Helvetica'
COLOR = "#102542"
BACKGROUND = '#CDD7D6'
BUTTON_COLOR = '#FFFFFF'
BUTTON_BG = "#102542"
HEIGHT = 200
WIDTH = 750
TEXTBOX_BACKGROUND = "#FFFFFF"
TEXTBOX_COLOR = "#102542"



def is_ffmpeg_available():
    try:
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")
        subprocess.run([ffmpeg_path, "-version"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    


class Transcriber:
    def __init__(self):
        self = self

    def set_ffmpeg_path(self):
    # Assuming the ffmpeg.exe is in the same directory as your main script
        ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")

        # Get the current PATH environment variable
        current_path = os.environ.get("PATH", "")

        # Append the directory containing the ffmpeg executable to the PATH
        os.environ["PATH"] = f"{current_path}{os.pathsep}{os.path.dirname(ffmpeg_path)}"

    def get_resource_path(self, relative_path):
        """Get the absolute path to the resource, works for development and PyInstaller"""
        if hasattr(sys, "_MEIPASS"):
            # If running as a PyInstaller executable, use sys._MEIPASS
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # If running as a regular Python script, use the current working directory
            return os.path.join(os.getcwd(), relative_path)
    def transcribe(self, file_path: str, language: str = "danish", model_size: str = "large"):
        try:
            model = whisper.load_model(model_size)
            if model:
                print(f"Model loaded succesfully")
            print(f"Transcribing file: {file_path}")
            transcription = model.transcribe(
                self.get_resource_path(file_path), language=language, fp16=False, verbose=True)
            if transcription:
                print("Transcription finished")
            return transcription
        except Exception as e:
            traceback.print_exc()
            print(f"Error during transcription: {e}")
            return None
        
    def float_to_time(self, float_value: float):
        milliseconds = int((float_value % 1) * 1000)
        seconds = int(float_value % 60)
        minutes = int((float_value // 60) % 60)
        hours = int(float_value // 3600)

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
        return time_str
    
    def output_to_text_file(self, data_dict: dict, output_file_name: str):
        index = 1
        try:
            with open(output_file_name, "w", encoding="utf-8") as file:
                for value in data_dict["segments"]:
                    start_time_str = self.float_to_time(value["start"])
                    end_time_str = self.float_to_time(value["end"])
                    text = value["text"].strip()
                    file.write(f"{index}\n")
                    file.write(f"{start_time_str} --> {end_time_str}\n")
                    file.write(f"{text}\n\n")
                    index = index + 1
        except Exception as e:
            print(f"Error during writing to text file: {e}")
    
    def allowed_file(self, filename, ALLOWED_EXTENSIONS):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_srt_name(self, file_path):
        try:
            if not self.allowed_file(file_path, ALLOWED_EXTENSIONS):
                raise ValueError("Invalid file type")
                
            srt_file = re.sub(r"\.[^.]+$", ".srt", os.path.basename(file_path))

            return srt_file

        except Exception as e:
            print(f"Error during creation of srt-file: {e}")
            return None
    

class Redirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        # Append the text to the Text widget
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)

transcriber = Transcriber()

class App(tk.Tk):
    def __init__(self):
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
                target=self.transcribe, args=(file_path,)
            )
            transcription_thread.start()

    def save_srt(self, srt_file, transcription):
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
                transcriber.output_to_text_file(
                    transcription, transcriber.get_resource_path(save_path)
                )
                # Show a success message to the user
                messagebox.showinfo("Fil Gemt", "Din SRT-fil er gemt!")


    def transcribe(self, file_path):
        try:
            transcription = transcriber.transcribe(transcriber.get_resource_path(file_path))
            srt_file = transcriber.get_srt_name(transcriber.get_resource_path(file_path))
            self.save_srt(srt_file, transcription)

        except Exception as e:
            # Show an error message to the user if something goes wrong
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Re-enable the button after transcription is done or if an error occurred
            sys.stdout = sys.__stdout__
            self.button.config(state=tk.NORMAL)


def main():
    transcriber.set_ffmpeg_path()
    print("Loading")

    if is_ffmpeg_available():
        print("ffmpeg is available!")
    else:
        print("ffmpeg is not available!")

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
