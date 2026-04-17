import os
import subprocess
import whisper
import torch

SUPPORTED_FORMATS = [".mp4", ".mov", ".webm", ".mkv"]


# Audio Extractor
def extract_audio(video_path, output_audio_path):
    try:
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-y",
            output_audio_path
        ]
        subprocess.run(command, check=True, capture_output=True)
        print(f"Audio extracted and saved to {output_audio_path}")
    except Exception as e:
        print(f"An error occurred during audio extraction: {e}")


# Speech Recognition
def transcribe_audio(audio_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("base", device=device)
    result = model.transcribe(audio_path)
    return result['segments']
