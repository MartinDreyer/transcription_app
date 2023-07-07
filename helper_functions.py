import whisper

def transcribe(file_path: str, language: str = "danish", model_size: str = "large"):
    model = whisper.load_model(model_size)
    transcription = model.transcribe(file_path, language=language, fp16=False, verbose=None)
    return transcription

def float_to_time(float_value: float):
    milliseconds = int((float_value % 1) * 1000)
    seconds = int(float_value % 60)
    minutes = int((float_value // 60) % 60)
    hours = int(float_value // 3600)
    
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    return time_str

def output_to_text_file(data_dict: dict, output_file_name: str):
    index = 1
    with open(output_file_name, "w", encoding="utf-8") as file:
        for value in data_dict["segments"]:
            start_time_str = float_to_time(value["start"])
            end_time_str = float_to_time(value["end"])
            text = value["text"].strip()
            file.write(f"{index}\n")
            file.write(f"{start_time_str} --> {end_time_str}\n")
            file.write(f"{text}\n\n")
            index = index + 1
        file.close()

