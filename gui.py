import tkinter as tk
from tkinter import filedialog
import threading
import requests
from transcriber import app as flask_app


class TranscriberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lyd til SRT")
        self.geometry("300x100")

        self.label = tk.Label(
            self, text="Upload en fil for at få den transskriberet")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="Vælg Fil",
                                command=self.handle_upload)
        self.button.pack(pady=5)

    def handle_upload():
        file_path = filedialog.askopenfilename()
        if file_path:
            files = {'file': open(file_path, 'rb')}
            response = requests.post(
                'http://localhost:5000/upload', files=files)
            if response.ok:
                response_text = response.text
                file_path = filedialog.asksaveasfilename(
                    title="Save file as", defaultextension=".srt")
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(response_text)


def run_flask_app():
    flask_app.run()


if __name__ == "__main__":
    # Run the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the Tkinter GUI
    app = TranscriberApp()
    app.mainloop()
