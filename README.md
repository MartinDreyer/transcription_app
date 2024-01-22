# T-tex

**T-tex** is a program for transcribing soundfiles to SubRip-format (.srt) in Danish. It is developed by TV 2 Fyn.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) (version: the app was developed using 3.11, but might run on other versions)
- [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today) (install using `pip install pipenv`)
- [ffmpeg](https://ffmpeg.org/download.html) (the ffmpeg.exe should be placed in the root folder, when the pyinstaller runs)

### Installation

```bash

# 1. Clone the repository
git clone https://github.com/MartinDreyer/transcription_app.git
cd transcription_app

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate virtual requirement
source .venv/Scripts/activate

# 4. Install requirements
pip install -r requirements.txt

# 5. Place ffmpeg.exe in root

# 6. Create executable
pyinstaller -n T-TEX --add-binary "ffmpeg.exe":"." --collect-data "whisper" --copy-metadata "openai-whisper" --collect-all "whisper"  app.py
```

### Running the Executable

After building the executable, you can run it as a regular .exe-file. You can also run it in the terminal. The .exe and \_internal folder should always be in the same directory.

### Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request. The app is under the GNU GENERAL PUBLIC LICENSE, please adhere to the terms of the license, which you can read in the LICENSE file.
