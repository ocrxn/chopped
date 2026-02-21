import os
import sys
import subprocess


class FileHandler():
    def __init__(self, filename, output_dir, args):
        self.filename = filename
        self.output_dir = output_dir
        self.args = args


    def compress_video(self):
        result = subprocess.run(["ls", "-l"], capture_output=True,text=True)
        return result.stdout

    def compress_audio(self):
        pass