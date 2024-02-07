"""
This program is a simple transcriber, that transcribes 
audio files and returns an SRT-file. The transcribing is
done by OpenAI"s Whisper model: https://github.com/openai/whisper

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
from tkinter import StringVar
import tkinter.filedialog as filedialog
import sys
import os
import traceback
import subprocess
import threading
from redirector import Redirector
from styling import *
from settings import *
import whisper
import tkinter.messagebox as messagebox
from openai import OpenAI



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("T-TEX")
        self.model_size = MODEL_SIZE
        self.output_dir = OUTPUT_DIR
        self.output_format = OUTPUT_FORMAT
        self.language = LANGUAGE
        self.ai_powered = True
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.line_breaks = True
        self.configure_grid(0, 1)
        self.configure_background(BACKGROUND)
        self.frame = self.create_frame(height=HEIGHT, width=WIDTH, background=BACKGROUND)
        self.label = self.create_label(labeltext="Vælg en fil for at få den transskriberet", background=BACKGROUND, color=COLOR, font=FONT, fontsize=LABEL_FONTSIZE, colpos=0, rowpos=0)
        self.select_button = self.create_button( buttontext="Vælg fil", pady=4, padx=8, width=int((WIDTH*0.05)), font=FONT, fontsize=12, background=BUTTON_BG, color=BUTTON_COLOR, command=self.handle_upload, activebackground=BUTTON_BG_ACTIVE, activeforeground=BUTTON_FG_ACTIVE, colpos=0, rowpos=2)
        self.transcribe_button = self.create_button( buttontext="Transkribér", pady=4, padx=8, width=int((WIDTH*0.05)), font=FONT, fontsize=12, background=BUTTON_BG, color=BUTTON_COLOR, command=self.start_transcription_thread, activebackground=BUTTON_BG_ACTIVE, activeforeground=BUTTON_FG_ACTIVE, colpos=0, rowpos=3)
        self.model_dropdown = self.create_dropdown(command=self.set_model_size, initial_option="Mellem", labeltext="Vælg modelstørrelse (mindre modeller er hurtigere, men transskriberingen er mindre præcis)", background=BACKGROUND, color=COLOR, font=FONT, fontsize=12, colpos=0, rowpos=4, relief="flat", cursor="hand2" ,options=[
            "Stor",
            "Mellem",
            "Lille",
            "Basal"
        ])
        self.line_dropdown = self.create_dropdown(command=self.set_line_length, labeltext="Vælg linjelængde", background=BACKGROUND, color=COLOR, font=FONT, fontsize=12, colpos=0, rowpos=6, options=['50 tegn', '60 tegn', '70 tegn'], initial_option=50, cursor="hand2", relief="flat")
        self.textbox = self.create_textbox(textbackground=TEXTBOX_BACKGROUND, textcolor=TEXTBOX_COLOR, font=FONT, fontsize=12, highlightbackground="#f2f2f2", colpos=0, rowpos=8)
        self.file_path = None
        self.current_file_label = self.create_label(labeltext=f"Valgt fil: {'Ingen' if self.file_path is None else self.file_path}", background=BACKGROUND, color=COLOR, font=FONT, fontsize=LABEL_FONTSIZE, colpos=0, rowpos=1)
        self.max_line_length = 50
        self.line = ''
        self.lines = []
        self.start_times = []
        self.start = ''
        self.end = ''
        self.redirector = Redirector(self.textbox)
        sys.stdout = self.redirector
        print(f"Running on {self.device}")


    def check_ffmpeg(self):
        try:
            
            ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
            subprocess.run([ffmpeg_path, '-version'], check=True)
            print("ffmpeg is available!")
            return True
        except subprocess.CalledProcessError:
            print("ffmpeg is not available!")
            return False

    def on_enter(self, event, button):
        button["bg"] = BUTTON_BG_HOVER

    def on_leave(self, event, button):
        button["bg"] = BUTTON_BG
    
    def configure_background(self, background):
        self.config(bg=background)

    def configure_grid(self, index, weight):
        self.rowconfigure(index=index, weight=weight)
        self.columnconfigure(index=index, weight=weight)

    def create_button(self, buttontext, pady, padx, width, background, color, font, fontsize, command, activebackground, activeforeground, colpos, rowpos):
        button = tk.Button(
            self, 
            text=buttontext,
            pady=pady,
            padx=padx,
            width=width,
            bg=background,
            fg=color,
            relief="flat",
            font=(font, fontsize),
            borderwidth=0,
            command=command,
            cursor="hand2",
            activebackground=activebackground,
            activeforeground=activeforeground
        )

        button.grid(column=colpos, row=rowpos, pady=(HEIGHT/10))
        button.bind("<Enter>", lambda event, button=button: self.on_enter(event, button))
        button.bind("<Leave>", lambda event, button=button: self.on_leave(event, button))

        return button
    
    def create_dropdown(self, command, labeltext, background, color, font, fontsize, colpos, rowpos, options, initial_option, cursor, relief):

        options = options

        clicked = StringVar()
        clicked.set(initial_option)
        dropdown = tk.OptionMenu(self,
                                      clicked,
                                      *options,
                                      command=command)
        
        self.create_label(labeltext=labeltext, background=BACKGROUND, color=COLOR, font=FONT, fontsize=DROPDOWN_LABEL_FONTSIZE, colpos=colpos, rowpos=rowpos)


        dropdown.grid(column=colpos, row=rowpos+1, pady=10, padx=10)
        dropdown.configure(
            padx=4,
            pady=8,
            font=(font, fontsize),
            relief=relief,
            cursor=cursor,
            bg=background,
            fg=color,
            borderwidth=0,
            width=int((WIDTH*0.01)),
        )

        return dropdown

    def create_frame(self, height, width, background):
        frame = tk.Frame(self, height=height, width=width, bg=background)
        frame.grid()
        return frame
    
    def create_label(self, labeltext, background, color, font, fontsize, colpos, rowpos):
        label = tk.Label(
        self, text=labeltext,
        bg=background,
        fg=color,
        font=(font, fontsize)
        )
        label.grid(column=colpos, row=rowpos)
        return label
    
    def create_textbox(self, textbackground, textcolor, font, fontsize, highlightbackground, colpos, rowpos):
        textbox = tk.Text(
            self,
            wrap=tk.WORD,
            bg=textbackground,
            fg=textcolor,
            borderwidth=0,
            padx=10,
            pady=10,
            font=(font, fontsize),
            highlightthickness=3,
        )
        textbox.config(highlightbackground=highlightbackground)
        textbox.grid(column=colpos, row=rowpos, pady=40, padx=40)

        return textbox
    
    def set_model_size(self, selected_option):
        if selected_option == "Stor":
            self.model_size = "large"
        elif selected_option == "Mellem":
            self.model_size = "medium"
        elif selected_option == "Lille":
            self.model_size = "small"
        elif selected_option == "Basal":
            self.model_size = "base"

    def set_line_length(self, selected_option):
        if selected_option == '70 tegn':
            self.max_line_length = 70
        elif selected_option == '60 tegn':
            self.max_line_length = 60
        elif selected_option == '50 tegn':
            self.max_line_length = 50

    def handle_upload(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path == '':
            return
        elif "." in self.file_path and self.file_path.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
            self.current_file_label.config(text=f"Valgt fil: {self.file_path.split('/')[-1]}")
        else:
            print(f"Forkert filtype. Følgende filtyper er godtaget: {ALLOWED_EXTENSIONS}")

    def set_ffmpeg_path(self):
        # Assuming the ffmpeg.exe is in the same directory as your main script
        ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")

        # Get the current PATH environment variable
        current_path = os.environ.get("PATH", "")

        # Append the directory containing the ffmpeg executable to the PATH
        os.environ["PATH"] = f"{current_path}{os.pathsep}{os.path.dirname(ffmpeg_path)}"

        return ffmpeg_path
    
    def optimize_file(self, file_path):
        try:
            output_filename = file_path.split(".")[0] + ".ogg"
            ffmpeg_path = self.set_ffmpeg_path()
            command = [
                ffmpeg_path,
                "-i", file_path,
                "-vn",
                "-map_metadata", "-1",
                "-ac", "1",
                "-c:a", "libopus",
                "-b:a", "12k",
                "-application", "voip",
                output_filename
            ]

            result = subprocess.run(command, shell=False)

            # Check the return code
            if result.returncode == 0:
                print(f"Converted inputfile to .ogg: {output_filename}")
                return output_filename
            else:
                print(
                    f"Error during conversion. Return code: {result.returncode}")
                print(result.stderr)

        except Exception as e:
            traceback.print_exc()
            print(f"Fejl under transskribering: {e}")
            return None       

    def start_transcription_thread(self):
            try:
                transcription_thread = threading.Thread(
                    target=self.transcribe, args=(self.file_path,)
                )
                transcription_thread.start()

            except Exception as e:
                traceback.print_exc()
                print(f"Error starting transcription thread: {e}")
    
    def get_resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return os.path.join(os.path.abspath("."), relative_path)

    
    def float_to_time(self, float_value: float):
        try:
            milliseconds = int((float_value % 1) * 1000)
            seconds = int(float_value % 60)
            minutes = int((float_value // 60) % 60)
            hours = int(float_value // 3600)

            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
            return time_str
        except Exception as e:
            traceback.print_exc()
            print(f"Error converting float to time format: {e}")

    
    def process_words(self, result, max_line_length=42, output_filename="output.srt"):
        all_words = []
        index = 0
        for value in result["segments"]:
            for word in value["words"]:
                all_words.append({
                    "id": index,
                    "word": word["word"],
                    "start": word["start"],
                    "end": word["end"]
                })
                index += 1
            
        return all_words

    def get_first_timecode(self, start_times):
        smallest = start_times[0]
        for val in start_times:
            if val < smallest:
                smallest = val
            
        return smallest
        
    def add_word(self, word, max_line_length):
        if self.line_breaks:
            word_text = word["word"]
            chars = [".", ",","!","?"]
            if any((c in chars) for c in word_text) and len(self.line) <= max_line_length:
                self.line += word_text
                self.end = word["end"]
                self.start_times.append(word["start"])
                start_time = self.get_first_timecode(self.start_times)
                self.lines.append({
                    "text": self.line,
                    "start": start_time,
                    "end": self.end
                })
                self.line = ""
                self.start_times = []
                return
            elif len(self.line) <= max_line_length:
                self.line += word_text
                self.end = word["end"]
                self.start_times.append(word["start"])
                return

            else:
                self.line += word_text
                start_time = self.get_first_timecode(self.start_times)
                self.lines.append({
                    "text": self.line,
                    "start": start_time,
                    "end": self.end
                })
                self.line = ""
                self.start_times = []
                return
    

    def create_srt(self, words_list, max_line_length, output_filename):
        for word in words_list:
            self.add_word(word, max_line_length)
        index = 1
        with open(output_filename, "w", encoding="utf-8") as f:
            for line in self.lines:
                start_time_str = self.float_to_time(line["start"])
                end_time_str = self.float_to_time(line["end"])
                text = line["text"].strip()
                f.write(f"{index}\n")
                f.write(f"{start_time_str} --> {end_time_str}\n")
                f.write(f"{text}\n\n")
                index += 1

    def validate_file_path(self, file_path):
        if file_path is not None:
            directory, filename = os.path.split(file_path)
            if os.path.exists(directory) and os.path.isfile(file_path):
                return True
        return False

    def transcribe_filepath(self, file_path):
        try:
            self.transcribe_button.config(state=tk.DISABLED)
            ogg_file = self.optimize_file(file_path)

            print(f'Loading {self.model_size.upper()} model')
            model = whisper.load_model(self.model_size, device=DEVICE)
            if model:
                print('Transcribing ...')
            result = model.transcribe(audio=self.get_resource_path(ogg_file), fp16=FP16, word_timestamps=TIMESTAMPS, verbose=VERBOSE)
            
            if ogg_file:
                os.remove(self.get_resource_path(ogg_file))
            self.transcribe_button.config(state=tk.NORMAL)
            
            return result
        except Exception as e:
            print(f'Error during transcription: {e}')

    def get_transcription(self, words, save_path):
        client = OpenAI( api_key="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")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[    
                {"role": "system", "content": "You are a subtitle generator. You will be provided with list of objects each containing a word, an id, a start time and an end time. You will produce a text in an srt-format. (i.e. ``1\n00:00:05,439 --> 00:00:06,459\nDet er en forkærlighed,\n\n2\n00:00:06,480 --> 00:00:06,780\nder har været,\n\n3\n00:00:06,839 --> 00:00:07,480\nsiden man var helt ung.\n\n4\n00:00:07,759 --> 00:00:09,800\nLigesom små børn kan lide traktorer,\n``) The lines must be no longer than 50 characters. You will also check for spelling mistakes. The srt file should be in danish. You will return only the text for the srt-file."},
                {"role": "user", "content": words}]
        )

        print(response.content)




    

    def save_transcription(self, result, file_path):
        try:
            directory, filename = os.path.split(file_path)
            save_path = filedialog.asksaveasfilename(
                title="Gem fil som", defaultextension=".srt", filetype=[("SubRip (.srt)", ".srt")], initialfile=(filename.split(".")[0] + "." + self.output_format)
            )
            words = self.process_words(result=result, output_filename=(os.path.join(directory, filename.split('.')[0] + '.' + self.output_format)), max_line_length=self.max_line_length)
            
            print(words)
            if save_path:
                if self.ai_powered:
                    self.get_transcription(words, save_path)
                
                else:
                    self.create_srt(words_list=words, max_line_length=self.max_line_length, output_filename=save_path)
                messagebox.showinfo("Fil Gemt", "Din SRT-fil er gemt!")
            print(f'{filename.split(".")[0] + "." + self.output_format} saved to {save_path} ')
            print('Transcription finished.')
        except IOError as e:
            print(f'Error during saving transcription: {e}')
            
            
    def transcribe(self, file_path):
        if self.validate_file_path(file_path) and self.check_ffmpeg():  
            print('Initializing')
            result = self.transcribe_filepath(file_path)
            if result:
                self.save_transcription(result, file_path)
        else:
            print("Invalid file path or ffmpeg not available.") 


def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
