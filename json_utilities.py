import os
from moviepy import VideoFileClip
from faster_whisper import WhisperModel
import logging

SUPPORTED_FORMATS = [".mp4", ".mov", ".webm", ".mkv"]

# Audio Extractor
def extract_audio(video_path, output_audio_path):
    try:
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(output_audio_path)
        logging.info(f"Audio extracted and saved to {output_audio_path}")
    except Exception as e:
        logging.error(f"An error occurred during audio extraction: {e}")
        return


# Speech Recognition

def transcribe_audio(audio_path):
    model = WhisperModel("base", device="cpu",compute_type="int8")
    segments,info = model.transcribe(audio_path)
    logging.info(f"[transcribe_audio] Language detected: {info.language} {info.language_probability:.0%}")
    segments = [{"start": s.start, "end": s.end, "text": s.text} for s in segments]
    return segments
