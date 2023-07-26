# main.py
import threading
import tkinter as tk
from tkinter import filedialog
import requests
import subprocess
import os
import sys


def run_flask_app():
    # Get the path to the current directory containing this script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the Flask app (assuming app.py is in the same directory)
    flask_app_path = os.path.join(current_dir, "transcriber.py")

    # Run the Flask app using the Python executable bundled in the executable
    subprocess.Popen([sys.executable, flask_app_path])


def handle_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        files = {'file': open(file_path, 'rb')}
        response = requests.post('http://localhost:5000/upload', files=files)
        if response.ok:
            response_text = response.text
            file_path = filedialog.asksaveasfilename(
                title="Save file as", defaultextension=".srt")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(response_text)


def main():
    print("Initializing")
    root = tk.Tk()

    print("Configuring window size")
    root.title("Lyd til SRT")
    root.geometry("400x400")

    upload_btn = tk.Button(root, text="Vælg Fil", command=handle_upload)
    upload_btn.pack(pady=20)
    print("Executing mainloop")
    root.mainloop()


if __name__ == "__main__":
    # Run the Flask app in a separate thread

    flask_thread = threading.Thread(target=run_flask_app)
    # Set the thread as daemon to stop when the main thread stops
    flask_thread.daemon = True
    flask_thread.start()
    main()
