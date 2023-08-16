# This file is part of NAVN.
#
# NAVN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 3, as published by
# the Free Software Foundation.
#
# NAVN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NAVN. If not, see <https://www.gnu.org/licenses/>.


import whisper
import sys
import os
import re
import traceback

# Set parameters
MODEL_SIZE = "large"
LANGUAGE = "danish"
ALLOWED_EXTENSIONS = ["wav", "mp3"]


def set_ffmpeg_path():
    # Assuming the ffmpeg.exe is in the same directory as your main script
    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")

    # Get the current PATH environment variable
    current_path = os.environ.get("PATH", "")

    # Append the directory containing the ffmpeg executable to the PATH
    os.environ["PATH"] = f"{current_path}{os.pathsep}{os.path.dirname(ffmpeg_path)}"


def get_resource_path(relative_path):
    """Get the absolute path to the resource, works for development and PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        # If running as a PyInstaller executable, use sys._MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # If running as a regular Python script, use the current working directory
        return os.path.join(os.getcwd(), relative_path)

def transcribe(file_path: str, language: str = "danish", model_size: str = "large"):
    try:
        model = whisper.load_model(model_size)
        if model:
            print(f"Model loaded succesfully: \n {model}")
        print(f"Transcribing file: {file_path}")
        transcription = model.transcribe(
            get_resource_path(file_path), language=language, fp16=False, verbose=False)
        if transcription:
            print("Transcription finished")
        return transcription
    except Exception as e:
        traceback.print_exc()
        print(f"Error during transcription: {e}")
        return None


def float_to_time(float_value: float):
    milliseconds = int((float_value % 1) * 1000)
    seconds = int(float_value % 60)
    minutes = int((float_value // 60) % 60)
    hours = int(float_value // 3600)

    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    return time_str


def output_to_text_file(data_dict: dict, output_file_name: str):
    index = 1
    try:
        with open(output_file_name, "w", encoding="utf-8") as file:
            for value in data_dict["segments"]:
                start_time_str = float_to_time(value["start"])
                end_time_str = float_to_time(value["end"])
                text = value["text"].strip()
                file.write(f"{index}\n")
                file.write(f"{start_time_str} --> {end_time_str}\n")
                file.write(f"{text}\n\n")
                index = index + 1
    except Exception as e:
        print(f"Error during writing to text file: {e}")


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_srt_name(file_path):
    try:
        if not allowed_file(file_path, ALLOWED_EXTENSIONS):
            raise ValueError("Invalid file type")
            
        srt_file = re.sub(r"\.[^.]+$", ".srt", os.path.basename(file_path))

        return srt_file

    except Exception as e:
        print(f"Error during creation of srt-file: {e}")
        return None

