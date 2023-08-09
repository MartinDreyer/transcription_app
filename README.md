# windowshvisker

**windowshvisker** is a program for transcribing soundfiles to SubRip-format (.srt) in Danish. It is developed by TV 2 Fyn.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) (version X.X or higher)
- [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today) (install using `pip install pipenv`)

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

After building the executable, you can run it in the terminal:

`./dist/Lyd til SRT.exe`

### Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.