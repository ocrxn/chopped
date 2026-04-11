#takes timestamps + labels and decides where clips start and end
from pathlib import Path
import json
import os
import random
from __future__ import annotations
import subprocess
from pathlib import Path
from config import BASE_DIR, CLIPS_FOLDER


#gets absolute path of current Python file and returns directory it’s located in; makes BASE_DIR a path
#__file__ is the path to the current Python file
#.resolve turns it into an absolute path
#.parent gets the folder containing the file
# BASE_DIR = Path(__file__).resolve().parent

#takes video + timestamps and cuts a clip
#uses FFmpeg
#cuts a highlight clip from a video
#uses FFmpeg when given a video path and timestamps
#takes in video file path
#takes in data from JSON file from processor.py
#uses JSON parameters
#uses ffmpeg to cut clips and put into folders

def clip_video(video_path: str, output_path: str, start_time: int, duration: int = 35):
    video_path = os.path.abspath(video_path)
    output_path = os.path.abspath(output_path)

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"input video not found: {video_path}")

    command = [
        "ffmpeg",
        "-ss", str(start_time),  # start cutting at start time
        "-i", video_path,  # input video file
        "-t", str(duration),  # duration of the cut
        "-c", "copy",  # copies audio and video streams without re-encoding
        "-y",  # so ffmpeg won't stop if file already exists
        output_path,  # output path for cut video file
    ]

    subprocess.run(command, check=True)
    os.remove(video_path)

#function to load events from .json file
def load_events(events_file):
    events_file = Path(events_file)

    #make sure filepath for file exists
    if not events_file.exists():
        raise Exception("file does not exist")

    # Open JSON file with exceptions
    try:
        # load JSON data in read mode
        with open(events_file, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
            raise Exception("Events JSON is not valid JSON")
            
    # check to make sure it's a list
    if not isinstance(data, list):
        raise Exception("Events JSON must be a list")
    
    return data

def matching_video(events_file, uploads_dir="uploads"): #debugged
    events_file=Path(events_file)
    uploads_dir = BASE_DIR / uploads_dir #combines base directory with uploads directory to create full path to uploads directory

    json_stem = events_file.stem # ex: takes game_0001 from game_0001.json

    possible_extensions = [".mp4", ".mov", ".webm", ".mkv"]
    
    for ext in possible_extensions:
         video_path = uploads_dir / f"{json_stem}{ext}"
         if video_path.exists():
              return video_path
    #for loop to iterate through uploads directory to see if a video matches  json file name
    
    raise FileNotFoundError(
         f"No matching video for {events_file.name} in {uploads_dir}"
    )

def process_video(events_file, clips_dir = "clips"):
     events_file = Path(events_file).resolve()
     clips_dir = Path(clips_dir).resolve()

     #match json file to video file
     video_path = matching_video(events_file)

     os.makedirs(clips_dir, exist_ok=True)
     events = load_events(events_file)
     #pass in data from json file
     
     folder_map = {
               #key -> value; dictionary to compare Python file to
               "hit": "hits",
               "out": "outs",
               "error": "errors",
               "bunt": "bunts",
               "pickoff": "pickoffs"
          }
     
     for i, event in enumerate(events):
        #loops through event in events but also keeps track of index i
                    
        event_type = event["type"]
        label = event["label"]
        time = event["timestamp"]
        num = random.randint(1000, 9999)

        folder_name = folder_map[event_type]
        #folder_map(event_type) means event type "hit" gives "hits"

        new_clips_dir = clips_dir / folder_name
        os.makedirs(new_clips_dir, exist_ok=True)

        output_path = new_clips_dir / f"{label}_{i+num}{video_path.suffix}"

        clip_video(
                 video_path=video_path, 
                 start_time= max(0, time - 8), 
                 duration=25, 
                 output_path=output_path
                 )
    
     os.remove(video_path)
     os.remove(events_file)

json_dir = BASE_DIR / "json"

def run_processor():
    """
    Runs the ffmpeg process to cut the clips from the video
    """
    for json_file in json_dir.glob("*.json"):
        #glob says must start with game_, * is a wildcard, and must end with .json (or whatever the filename is)
        try:
            game_clips_dir = os.path.join(CLIPS_FOLDER, json_file.stem)
            #process_video will make a new directory within the clips folder
            #it will have the name of json_file.stem
            process_video(json_file, clips_dir = game_clips_dir)
                
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
