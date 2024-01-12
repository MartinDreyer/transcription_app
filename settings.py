import torch


# Transcriber settings
LANGUAGE = 'da'
ALLOWED_EXTENSIONS = ['wav', 'mp3', 'mp4', 'mpga', 'webm', 'm4a']
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_SIZE = 'medium'
VERBOSE = 'True'
OUTPUT_FORMAT = 'srt'
LINE_COUNT = '1'
LINE_WIDTH = '42'
TIMESTAMPS = 'True'
FP16 = 'True' if torch.cuda.is_available() else 'False'
