# transcription.py
from helper_functions import transcribe, allowed_file
import os
import re
from dotenv import load_dotenv
import os
import re


load_dotenv()


MODEL_SIZE = os.getenv("MODEL_SIZE")
LANGUAGE = os.getenv("LANGUAGE")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


def transcribe_and_generate_srt(file_path):
    try:
        if not allowed_file(file_path, ALLOWED_EXTENSIONS):
            raise ValueError("Invalid file type")

        print("Transcribing file")
        transcription = transcribe(file_path, LANGUAGE, MODEL_SIZE)
        srt_file = re.sub(r"\.[^.]+$", ".srt", os.path.basename(file_path))

        return transcription, srt_file

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
