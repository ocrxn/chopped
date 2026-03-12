#cuts a highlight clip from a video
#uses FFmpeg when given a video path and timestamps

from __future__ import annotations

import subprocess #lets Python run other programs on computer (FFmpeg)
from pathlib import Path #necessary for working with file paths
import json
from processor import load_events



def clip_video(video_path: str, output_path: str, start_time: int, duration: int = 35):
    
    json_file = Path("data.json")
    load_events(json_file)


    command = [
        "ffmpeg",
        "-i", video_path, #input video file
        "-ss", str(start_time), #start cutting at start time
        "-t", str(duration), #duration of the cut
        "-c", "copy", #copies audio and video streams without re-encoding
                      #makes process faster
        output_path #output path for cut video file
    ]

    subprocess.run(command, check=True)
    

#takes in video file path
#takes in data from JSON file from processor.py
#uses JSON parameters
#uses ffmpeg to cut clips and put into folders