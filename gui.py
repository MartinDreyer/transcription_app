import tkinter as tk
import tkinter.filedialog as filedialog
from transcriber import transcribe_and_generate_srt
from helper_functions import output_to_text_file
import os
import threading
import tkinter.messagebox as messagebox
import re


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
            transcription, srt_file = transcribe_and_generate_srt(file_path)
            if transcription:
                # Ask the user to specify the save location
                save_path = filedialog.asksaveasfilename(
                    title="Save file as", defaultextension=".srt", filetype=[("SubRip (.srt)", ".srt")], initialfile=srt_file
                )
                if save_path:
                    # Save the content directly to the user-specified location
                    output_to_text_file(transcription, save_path)
                    # Show a success message to the user
                    messagebox.showinfo("Fil Gemt", "Din SRT-fil er gemt!")
        except Exception as e:
            # Show an error message to the user if something goes wrong
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Re-enable the button after transcription is done or if an error occurred
            self.button.config(state=tk.NORMAL)

def main():
    app = TranscriberApp()
    app.mainloop()

if __name__ == "__main__":
    main()
