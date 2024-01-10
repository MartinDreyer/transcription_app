import torch


# Transcriber settings
LANGUAGE = 'danish'
ALLOWED_EXTENSIONS = ['wav', 'mp3', 'mp4', 'mpga', 'webm', 'm4a']
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_SIZE = 'medium'
VERBOSE = 'True'
OUTPUT_FORMAT = 'srt'
LINE_COUNT = '1'
TIMESTAMPS = 'True'
