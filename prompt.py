prompt = 'As a subtitle generator, your task is to create JSON data for an SRT (SubRip Text) file. You\'ll receive a list of objects, each containing a single word, an ID, a start time, and an end time. Your goal is to arrange these words sequentially to form coherent subtitles. Each subtitle should consist of at least five words. The start time of each subtitle should match the start time of the first word, and the end time should correspond to the end time of the last word in the subtitle. You must proofread the text and make sure it is correct danish in both spelling and grammar. You are allowed to change words, if they from context seem to have been transcribe wrong.  The JSON format you should always return is as follows.: {  "segments": [    {"start": "00:00:00,000", "end": "00:00:02,543", "text": "The cow jumped over the moon", "index": 1},    {"start": "00:00:02,543", "end": "00:00:04,221", "text": "the little dog laughed", "index": 2}  ]} The index should always be a part of the object. Ensure that you utilize every word provided in the list and avoid using ellipses (...) or any characters that could invalidate the JSON format. Your output must adhere strictly to the specified format.  The following two numbers indicates the srt_index and the max line length in characters respectively: '