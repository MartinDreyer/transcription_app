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
from tkinter import StringVar
import sys
from styling import *
from settings import *
from redirector import Redirector
import tkinter.filedialog as filedialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("T-TEX")
        self.model_size = MODEL_SIZE
        self.configure_grid(0, 1)
        self.configure_background(BACKGROUND)
        self.frame = self.create_frame(height=HEIGHT, width=WIDTH, background=BACKGROUND)
        self.label = self.create_label(labeltext="Vælg en fil for at få den transskriberet", background=BACKGROUND, color=COLOR, font=FONT, fontsize=LABEL_FONTSIZE, colpos=0, rowpos=0)
        self.select_button = self.create_button( buttontext="Vælg fil", pady=4, padx=8, width=int((WIDTH*0.05)), font=FONT, fontsize=12, background=BUTTON_BG, color=BUTTON_COLOR, command=self.handle_upload, activebackground=BUTTON_BG_ACTIVE, activeforeground=BUTTON_FG_ACTIVE)
        self.dropdown = self.create_dropdown(command=self.set_model_size, background=BACKGROUND, color=COLOR, font=FONT, fontsize=12)
        self.textbox = self.create_textbox(textbackground=TEXTBOX_BACKGROUND, textcolor=TEXTBOX_COLOR, font=FONT, fontsize=12, highlightbackground="#f2f2f2")

    def on_enter(self, e):
        self.select_button["bg"] = BUTTON_BG_HOVER

    def on_leave(self, e):
        self.select_button["bg"] = BUTTON_BG
    
    def configure_background(self, background):
        self.config(bg=background)

    def configure_grid(self, index, weight):
        self.rowconfigure(index=index, weight=weight)
        self.columnconfigure(index=index, weight=weight)

    def create_button(self, buttontext, pady, padx, width, background, color, font, fontsize, command, activebackground, activeforeground):
        button = tk.Button(
            self, 
            text=buttontext,
            pady=pady,
            padx=padx,
            width=width,
            bg=background,
            fg=color,
            relief='flat',
            font=(font, fontsize),
            borderwidth=0,
            command=command,
            cursor='hand2',
            activebackground=activebackground,
            activeforeground=activeforeground
        )

        button.grid(column=0, row=1, pady=(HEIGHT/10))
        button.bind('<Enter>', self.on_enter)
        button.bind('<Leave>', self.on_leave)

        return button
    
    def create_dropdown(self, command, background, color, font, fontsize):
        options = [
            "Stor",
            "Mellem",
            "Lille",
            "Basal"
        ]
        clicked = StringVar()
        clicked.set("Mellem")
        dropdown = tk.OptionMenu(self,
                                      clicked,
                                      *options,
                                      command=command)

        setting_label = tk.Label(
            self, text='Vælg modelstørrelse (mindre modeller er hurtigere, men transskriberingen er mindre præcis)',
            bg=background,
            fg=color,
            font=(font, (fontsize - 2))
        )
        setting_label.grid(column=0, row=2)

        dropdown.grid(column=0, row=3, pady=10, padx=10)
        dropdown.configure(
            padx=4,
            pady=8,
            font=(font, fontsize),
            relief="flat",
            cursor='hand2',
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
    
    def create_textbox(self, textbackground, textcolor, font, fontsize, highlightbackground):
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
        textbox.grid(column=0, row=4, pady=40, padx=40)
        sys.stdout = Redirector(textbox)

        return textbox
    
    def set_model_size(self, selected_option):
        print(selected_option)
        if selected_option == "Stor":
            self.MODEL_SIZE = "large"
        elif selected_option == "Mellem":
            self.MODEL_SIZE = "medium"
        elif selected_option == "Lille":
            self.MODEL_SIZE = "small"
        elif selected_option == "Basal":
            self.MODEL_SIZE = "base"

    def handle_upload(self):
        file_path = filedialog.askopenfilename()
        



def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
