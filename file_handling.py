import os
import sys
import subprocess
import time
from datetime import datetime


class FileHandler():
    def __init__(self):
        pass

    def compress_video(self, kwargs):
        filename = kwargs.get("filename")
        input_path = kwargs.get("input_path")
        audio_format = kwargs.get("audio_format")
        output_format = kwargs.get("output_format") or "mp4"
        output_dir = kwargs.get("output_dir")

        if not filename or not input_path:
            return
        
        os.makedirs(output_dir, exist_ok=True)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"cmpr_{name}.{output_format}")

        video_codec_map = {
            "mp4": "libx264",
            "mkv": "libx265",
            "webm": "libvpx-vp9",
            "mov": "libx264"
        }
        audio_codec_map = {
            "mp4": "aac",
            "mkv": "aac",
            "webm": "libopus",
            "mov": "aac"
        }

        video_codec = video_codec_map.get(output_format, "libx264")
        audio_codec = audio_codec_map.get(output_format, "aac")

        original_size = os.path.getsize(input_path)
        start_time = time.perf_counter()

        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vf", "scale='min(1280,iw)':-2",
            "-c:v", video_codec,
            "-crf", "28",
            "-preset", "slow",
            "-c:a", audio_codec,
            "-b:a", "64k",
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        # Get compressed file size
        if os.path.exists(output_path):
            compressed_size = os.path.getsize(output_path)
            ratio = original_size / compressed_size
        else:
            compressed_size = 0
            ratio = 0

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_text = (
        f"[{timestamp}] File: {filename}\n"
        f"Original size: {original_size / 1024:.2f} KB\n"
        f"Compressed size: {compressed_size / 1024:.2f} KB\n"
        f"Compression ratio: {ratio:.2f}x smaller\n"
        f"Time taken: {elapsed:.2f} seconds\n"
        "----------------------------------------\n"
    )
        log_file_path = os.path.join(output_dir, "compression_log.txt")
        with open(log_file_path, "a") as f:
            f.write(log_text)

        return result
        
    def compress_audio(self):
        pass