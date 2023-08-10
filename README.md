# windowshvisker

**windowshvisker** is a program for transcribing soundfiles to SubRip-format (.srt) in Danish. It is developed by TV 2 Fyn.

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
  pipenv install

  # 3. Create the .exe-file
  pipenv run pyinstaller gui.spec
  ```

### Running the Executable

After building the executable, you can run it as a regulare .exe-file. You can also run it in the terminal:

`./dist/Lyd til SRT.exe`

### Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request. The app is under the  GNU GENERAL PUBLIC LICENSE, please adhere to the terms of the license, which you can read in the LICENSE file. 
