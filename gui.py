# gui.py
import tkinter as tk
from tkinter import filedialog
from transcriber import transcribe_and_generate_srt
import os


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
            srt_file = transcribe_and_generate_srt(file_path)
            if srt_file:
                file_path = filedialog.asksaveasfilename(
                    title="Save file as", defaultextension=".srt")
                if file_path:
                    # Copy the generated SRT file to the user-specified location
                    with open(srt_file, "r", encoding="utf-8") as src_file:
                        with open(file_path, "w", encoding="utf-8") as dest_file:
                            dest_file.write(src_file.read())
                    # Remove the temporary SRT file
                    os.remove(srt_file)


def main():
    app = TranscriberApp()
    app.mainloop()


if __name__ == "__main__":
    main()
