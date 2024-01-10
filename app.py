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
import whisper
import traceback
import re
import torch

# Transcriber settings
MODEL_SIZE = 'large'
LANGUAGE = 'danish'
ALLOWED_EXTENSIONS = ['wav', 'mp3', 'mp4', 'mpga', 'webm', 'm4a']
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# GUI Styling
FONT = 'Helvetica'
COLOR = '#102542'
BACKGROUND = '#f7f7f7'
BUTTON_COLOR = '#FFFFFF'
BUTTON_BG = '#102542'
BUTTON_BG_HOVER = "#006dbd"
BUTTON_BG_ACTIVE = "#6eb3e6"
HEIGHT = 200
WIDTH = 750
TEXTBOX_BACKGROUND = '#FFFFFF'
TEXTBOX_COLOR = '#102542'



def is_ffmpeg_available():
    try:
        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
        subprocess.run([ffmpeg_path, '-version'], check=True)
        print(ffmpeg_path)
        return True
    except subprocess.CalledProcessError:
        return False
    


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
                print(f"Error during conversion. Return code: {result.returncode}")
                print(result.stderr)
            
            
        except Exception as e:
            traceback.print_exc()
            print(f'Fejl under transskribering: {e}')
            return None
        
    def transcribe(self, file_path: str, language: str = 'da', model_size: str = 'base'):
        self.optimize_file(file_path)
        try:
            OUTPUT_DIR = os.path.dirname(file_path)
            command = [
                'whisper', 
                file_path,
                '--language', 
                language, 
                '--model', 
                model_size, 
                '--output_dir', 
                OUTPUT_DIR, 
                '--device', 
                DEVICE,
                '--word_timestamps',
                'True',
                '--max_line_count',
                '1',
                '--output_format',
                "srt"
            ]
        
            result = subprocess.run(
                command, 
                capture_output=True,
                shell=False)
            
            self.textbox = Redirector(result.stdout)
            # Check the return code
            if result.returncode == 0:
                print(f"Transcription successful.")
                print(f"Result: {result.stdout}")

            else:
                print(f"Error during transcription. Return code: {result.returncode}")
                print(result.stderr)
        except Exception as e:
            print(f"Error during transcription: {e}")




    def allowed_file(self, filename, ALLOWED_EXTENSIONS):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_srt_name(self, file_path):
        try:
            if not self.allowed_file(file_path, ALLOWED_EXTENSIONS):
                raise ValueError('Ikke tilladt filtype')
                
            srt_file = re.sub(r'\.[^.]+$', '.srt', os.path.basename(file_path))

            return srt_file

        except Exception as e:
            print(f'Fejl ved skrivning til srt-fil: {e}')
            return None
    

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
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.transcriber = Transcriber()


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
            relief= 'flat', 
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
            "large",
            "medium",
            "small", 
            "base"
        ]

        self.clicked = StringVar()
        self.clicked.set("large")

        self.dropdown = tk.OptionMenu(self, self.clicked, *options)
        self.dropdown.grid(column=0, row=3, pady=40, padx=40)

    
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
        self.textbox.grid(column=0, row=2, pady=40, padx=40)
        self.textbox.insert(INSERT, 'Mens programmet arbejder, bliver din transskribering vist her. \n')
        sys.stdout = Redirector(self.textbox)

    def on_enter(self, e):
        self.button["bg"] = BUTTON_BG_HOVER

    def on_leave(self, e):
        self.button["bg"] = BUTTON_BG

    def set_model_size(self):
        MODEL_SIZE = self.clicked.get()
    
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
                title='Gem fil som',
                defaultextension='.srt',
                filetype=[('SubRip (.srt)', '.srt')],
                initialfile=srt_file,
            )


    def transcribe(self, file_path):
        try:
            print(f"Transcribing {file_path} using {MODEL_SIZE} model")
            transcription = self.transcriber.transcribe(self.transcriber.get_resource_path(file_path))
            srt_file = self.transcriber.get_srt_name(self.transcriber.get_resource_path(file_path))
            self.save_srt(srt_file, transcription)

        except Exception as e:
            # Show an error message to the user if something goes wrong
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

        finally:
            # Re-enable the button after transcription is done or if an error occurred
            sys.stdout = sys.__stdout__
            self.button.config(state=tk.NORMAL)


def main():
    print('Loading')

    if is_ffmpeg_available():
        print('ffmpeg is available!')
    else:
        print('ffmpeg is not available!')
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
