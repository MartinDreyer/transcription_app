from flask import Flask, request, current_app
from werkzeug.utils import secure_filename
from flask_cors import CORS
from helper_functions import output_to_text_file, transcribe
from dotenv import load_dotenv
import os
import re

load_dotenv()
MODEL_SIZE = os.getenv("MODEL_SIZE")
LANGUAGE = os.getenv("LANGUAGE")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'No file uploaded', 400

        f = request.files['file']
        if f.filename == '':
            return 'No file selected', 400
        
        
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            # Save the file to a desired location
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            
            srt_file = re.sub(r"\.[^.]+$", ".srt", os.path.join(app.config['UPLOAD_FOLDER'], filename))
            srt_file_name = re.sub(r"\.[^.]+$", ".srt", filename)

            transcription = transcribe(os.path.join(app.config['UPLOAD_FOLDER'], filename), LANGUAGE, MODEL_SIZE)
            output_to_text_file(transcription, srt_file)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        def generate():
                with open(srt_file) as f:
                    yield from f

                os.remove(srt_file)

        r = current_app.response_class(generate(), mimetype='text/srt')
        r.headers.set('Content-Disposition', 'attachment', filename=srt_file_name)
        return r
    except:
        return "Something went wrong", 500


if __name__ == '__main__':
    app.run()