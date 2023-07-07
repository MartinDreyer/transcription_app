from flask import Flask, request, send_file
from flask_cors import CORS
from helper_functions import output_to_text_file, transcribe
from dotenv import load_dotenv
import os
import re

load_dotenv()
MODEL_SIZE = os.getenv("MODEL_SIZE")
LANGUAGE = os.getenv("LANGUAGE")


app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'No file uploaded', 400

        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400

        # Save the file to a desired location
        file.save(file.filename)

        output_file_name = re.sub(r"\.[^.]+$", ".srt",file.filename)
        transcription = transcribe(file.filename, LANGUAGE, MODEL_SIZE)
        output_to_text_file(transcription, output_file_name)

        response = send_file(output_file_name, as_attachment=True)
        os.remove(output_file_name)
        os.remove(file.filename)
        return response
    except:
        return Exception("Something went wrong")


if __name__ == '__main__':
    app.run(debug=False)