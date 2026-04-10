import os
from moviepy import VideoFileClip
import whisper

SUPPORTED_FORMATS = [".mp4", ".mov", ".webm", ".mkv"]

# Audio Extractor
def extract_audio(video_path, output_audio_path):
    try:
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(output_audio_path)
        print(f"Audio extracted and saved to {output_audio_path}")
    except Exception as e:
        print(f"An error occurred during audio extraction: {e}")


# Speech Recognition

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['segments']
