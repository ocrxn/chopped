import os
import sys
import subprocess


class FileHandler():
    def __init__(self):
        pass

    def compress_video(self, kwargs):
        filename = kwargs.get("filename")
        if not filename:
            return
        
        output_name = f"cmpr_{filename}.{kwargs.get("output_format", "mp4")}"

        result = subprocess.run(["ffmpeg", "-i", filename, 
                                 "-vf", "scale=1280:-2",
                                   "-vcodec", "libx264",
                                     "-crf", "28",
                                       output_name],
                                         capture_output=True,text=True)
        return result
        
    def compress_audio(self):
        pass