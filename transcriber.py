from flask import Flask, current_app, jsonify, request
from werkzeug.utils import secure_filename
from helper_functions import output_to_text_file, transcribe, allowed_file
from dotenv import load_dotenv
import os
import re


load_dotenv()
MODEL_SIZE = os.getenv("MODEL_SIZE")
LANGUAGE = os.getenv("LANGUAGE")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

# Define your Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify(error='No file uploaded'), 400

        f = request.files['file']

        if f.filename == '':
            return jsonify(error='No file selected'), 400

        if f and allowed_file(f.filename, ALLOWED_EXTENSIONS):
            print("Saving file")
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            srt_file = re.sub(
                r"\.[^.]+$", ".srt", os.path.join(app.config['UPLOAD_FOLDER'], filename))
            srt_file_name = re.sub(r"\.[^.]+$", ".srt", filename)

            try:
                print("Transcribing file")
                transcription = transcribe(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename), LANGUAGE, MODEL_SIZE)
            except Exception as e:
                print(f"Error during transcription: {e}")
                return jsonify(error='Something went wrong during transcription'), 500

            print("Creating srt-file")
            output_to_text_file(transcription, srt_file)

            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            def generate():
                with open(srt_file) as f:
                    yield from f

                os.remove(srt_file)

            r = current_app.response_class(generate(), mimetype='text/srt')
            r.headers.set('Content-Disposition', 'attachment',
                          filename=srt_file_name)
            return r
        else:
            return jsonify(error='Invalid file type'), 400

    except Exception as e:
        print(f"Error during file upload: {e}")
        return jsonify(error='Something went wrong'), 500


if __name__ == "__main__":
    # Run the Flask app in a separate thread
    app.run()
