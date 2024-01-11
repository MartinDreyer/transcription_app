'''
This program is a simple transcriber, that transcribes 
audio files and returns an SRT-file. The transcribing is
done by OpenAI's Whisper model: https://github.com/openai/whisper

This code bundles into an .exe-file that runs on Windows. It is developed on a Windows 11 machine, 
but has run succesfully on Windows 7 and 10 machines.

Author: Martin Dreyer
'''

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
from tkinter import INSERT
from tkinter import StringVar
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import threading
import os
import subprocess
import sys
import traceback
from styling import *
from settings import *



class Transcriber:
    def __init__(self):
        self = self
    def set_ffmpeg_path(self):
    # Assuming the ffmpeg.exe is in the same directory as your main script
        ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg.exe')

        # Get the current PATH environment variable
        current_path = os.environ.get('PATH', '')

        # Append the directory containing the ffmpeg executable to the PATH
        os.environ['PATH'] = f'{current_path}{os.pathsep}{os.path.dirname(ffmpeg_path)}'

        return ffmpeg_path

    def get_resource_path(self, relative_path):
        '''Get the absolute path to the resource, works for development and PyInstaller'''
        if hasattr(sys, '_MEIPASS'):
            # If running as a PyInstaller executable, use sys._MEIPASS
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            # If running as a regular Python script, use the current working directory
            return os.path.join(os.getcwd(), relative_path)

    def optimize_file(self, file_path):
        try:
            output_filename = file_path.split(".")[0] + '.ogg'
            ffmpeg_path = self.set_ffmpeg_path()
            command = [
                ffmpeg_path,
                '-i', file_path,
                '-vn',
                '-map_metadata', '-1',
                '-ac', '1',
                '-c:a', 'libopus',
                '-b:a', '12k',
                '-application', 'voip',
                output_filename
            ]

            result = subprocess.run(command, shell=False)

            # Check the return code
            if result.returncode == 0:
                print(f"Conversion successful. Output file: {output_filename}")
            else:
                print(
                    f"Error during conversion. Return code: {result.returncode}")
                print(result.stderr)

        except Exception as e:
            traceback.print_exc()
            print(f'Fejl under transskribering: {e}')
            return None

    def transcribe(self, file_path: str, language: str = 'da', model_size: str = 'base'):
        self.optimize_file(file_path)

        try:
            ffmpeg_path = self.set_ffmpeg_path()
            print(f'FFMPEG-path: {ffmpeg_path}')
            OUTPUT_DIR = os.path.dirname(self.get_resource_path(file_path))
            command = [
                'whisper',
                self.get_resource_path(file_path.split(".")[0] + ".ogg"),
                '--language',
                language,
                '--model',
                model_size,
                '--output_dir',
                OUTPUT_DIR,
                '--device',
                DEVICE,
                '--word_timestamps',
                TIMESTAMPS,
                '--max_line_count',
                LINE_COUNT,
                '--max_line_width',
                LINE_WIDTH,
                '--output_format',
                OUTPUT_FORMAT,
                '--verbose',
                VERBOSE,
                '--fp16',
                FP16
            ]
            print(f"Running command {command}")

            result = subprocess.run(
                command,
                shell=False)

            if result.returncode == 0:
                print(f"Transcription successful.")
                os.remove(file_path.split(".")[0] + ".ogg")

            else:
                print(
                    f"Error during transcription. Return code: {result.returncode}")
                print(result.stderr)
        except Exception as e:
            print(f"Error during transcription: {e}")

    def allowed_file(self, filename, ALLOWED_EXTENSIONS):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Redirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        # Append the text to the Text widget
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame = tk.Frame(self, height=HEIGHT, width=WIDTH)
        self.frame.config(bg=BACKGROUND, )
        self.config(bg=BACKGROUND)
        self.title('T-TEX')
        self.frame.grid()

        self.transcriber = Transcriber()
        self.MODEL_SIZE = MODEL_SIZE
        self.label = tk.Label(
            self, text='Vælg en fil for at få den transskriberet',
            bg=BACKGROUND,
            fg=COLOR,
            font=(FONT, 14)
        )
        self.label.grid(column=0, row=0)

        self.button = tk.Button(
            self,
            text='Vælg Fil',
            pady=4,
            padx=8,
            width=int((WIDTH*0.05)),
            bg=BUTTON_BG,
            fg=BUTTON_COLOR,
            relief='flat',
            font=(FONT, 12),
            borderwidth=0,
            command=self.handle_upload,
            cursor='hand2',
            activebackground=BUTTON_BG_ACTIVE,
            activeforeground=BUTTON_COLOR
        )

        self.button.grid(column=0, row=1, pady=(HEIGHT/10))
        self.button.bind('<Enter>', self.on_enter)
        self.button.bind('<Leave>', self.on_leave)

        options = [
            "Stor",
            "Mellem",
            "Lille",
            "Basal"
        ]

        self.clicked = StringVar()
        self.clicked.set("Mellem")

        def set_model_size(selected_option):
            if selected_option == "Stor":
                self.MODEL_SIZE = "large"
            elif selected_option == "Mellem":
                self.MODEL_SIZE = "medium"
            elif selected_option == "Lille":
                self.MODEL_SIZE = "small"
            elif selected_option == "Basal":
                self.MODEL_SIZE = "base"

        self.dropdown = tk.OptionMenu(self,
                                      self.clicked,
                                      *options,
                                      command=set_model_size)

        self.setting_label = tk.Label(
            self, text='Vælg modelstørrelse (mindre modeller er hurtigere, men transskriberingen er mindre præcis)',
            bg=BACKGROUND,
            fg=COLOR,
            font=(FONT, 10)
        )
        self.setting_label.grid(column=0, row=2)

        self.dropdown.grid(column=0, row=3, pady=10, padx=10)
        self.dropdown.configure(
            padx=4,
            pady=8,
            font=(FONT, 12),
            relief="flat",
            cursor='hand2',
            bg="#333333",
            fg="#eeeeee",
            borderwidth=0,
            width=int((WIDTH*0.01)),
        )

        self.textbox = tk.Text(
            self,
            wrap=tk.WORD,
            bg=TEXTBOX_BACKGROUND,
            fg=TEXTBOX_COLOR,
            borderwidth=0,
            padx=10,
            pady=10,
            font=(FONT, 12),
            highlightthickness=3,
        )
        self.textbox.config(highlightbackground="#f2f2f2")
        self.textbox.grid(column=0, row=4, pady=40, padx=40)
        sys.stdout = Redirector(self.textbox)

    def on_enter(self, e):
        self.button["bg"] = BUTTON_BG_HOVER

    def on_leave(self, e):
        self.button["bg"] = BUTTON_BG

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

    def transcribe(self, file_path):
        try:
            print(f"Transcribing {file_path} using {self.MODEL_SIZE} model")
            self.transcriber.transcribe(self.transcriber.get_resource_path(
                file_path), model_size=self.MODEL_SIZE)

        except Exception as e:
            # Show an error message to the user if something goes wrong
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

        finally:
            # Re-enable the button after transcription is done or if an error occurred
            sys.stdout = sys.__stdout__
            self.button.config(state=tk.NORMAL)


def main():
    transcriber = Transcriber()
    transcriber.set_ffmpeg_path()
    
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
