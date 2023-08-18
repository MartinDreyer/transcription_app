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
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import helper_functions as hf
import threading
import os
import subprocess


def is_ffmpeg_available():
    try:
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")
        subprocess.run([ffmpeg_path, '-version'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False



class TranscriberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lyd til SRT")
        self.geometry("300x100")

        self.label = tk.Label(
            self, text="Vælg en fil for at få den transskriberet")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Vælg Fil",
                                command=self.handle_upload)
        self.button.pack(pady=5)

    def handle_upload(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Disable the button to avoid multiple clicks during transcription
            self.button.config(state=tk.DISABLED)

            # Start the transcription task in a separate thread
            transcription_thread = threading.Thread(target=self.transcribe_and_save_srt, args=(file_path,))
            transcription_thread.start()

    def transcribe_and_save_srt(self, file_path):
        try:
            transcription = hf.transcribe(hf.get_resource_path(file_path))
            srt_file = hf.get_srt_name(hf.get_resource_path(file_path))
            if transcription:
                # Ask the user to specify the save location
                save_path = filedialog.asksaveasfilename(
                    title="Gem fil som", defaultextension=".srt", filetype=[("SubRip (.srt)", ".srt")], initialfile=srt_file
                )
                if save_path:
                    # Save the content directly to the user-specified location
                    hf.output_to_text_file(transcription, hf.get_resource_path(save_path))
                    # Show a success message to the user
                    messagebox.showinfo("Fil Gemt", "Din SRT-fil er gemt!")
        except Exception as e:
            # Show an error message to the user if something goes wrong
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Re-enable the button after transcription is done or if an error occurred
            self.button.config(state=tk.NORMAL)

def main():
    hf.set_ffmpeg_path()
    print("Loading")

    if is_ffmpeg_available():
        print("ffmpeg is available!")
    else:
        print("ffmpeg is not available!")


    app = TranscriberApp()
    app.mainloop()

if __name__ == "__main__":
    main()
