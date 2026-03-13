import os
import json
from utilities import find_and_convert_video, extract_audio, transcribe_audio, ProgressTracker

# Map each phrase to its type and label for the JSON output
trigger_phrases = {
    "double play": {"type": "hit", "label": "Double Play"},
    "strikeout": {"type": "out", "label": "Strikeout"},
    "groundout": {"type": "out", "label": "Groundout"},
    "flyout": {"type": "out", "label": "Flyout"},
    "single": {"type": "hit", "label": "Single"},
    "double": {"type": "hit", "label": "Double"},
    "triple": {"type": "hit", "label": "Triple"},
    "walk": {"type": "hit", "label": "Walk"},
    # Positional errors E1-E9
    "e1": {"type": "error", "label": "E1 - Pitcher"},
    "e2": {"type": "error", "label": "E2 - Catcher"},
    "e3": {"type": "error", "label": "E3 - First Base"},
    "e4": {"type": "error", "label": "E4 - Second Base"},
    "e5": {"type": "error", "label": "E5 - Third Base"},
    "e6": {"type": "error", "label": "E6 - Shortstop"},
    "e7": {"type": "error", "label": "E7 - Left Field"},
    "e8": {"type": "error", "label": "E8 - Center Field"},
    "e9": {"type": "error", "label": "E9 - Right Field"},
    "error": {"type": "error", "label": "Error"},
}

# Sort longest first so "double play" is matched before "double"
sorted_phrases = sorted(trigger_phrases.keys(), key=len, reverse=True)


def find_trigger_segments(segments):
    matches = []
    for segment in segments:
        text_lower = segment['text'].lower()
        for phrase in sorted_phrases:
            if phrase in text_lower:
                matches.append({
                    "type": trigger_phrases[phrase]["type"],
                    "timestamp": round(segment['start']),
                    "label": trigger_phrases[phrase]["label"]
                })
                break
    return matches


def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted {path}")
    except PermissionError:
        print(f"Could not delete {path} — you can delete it manually.")


def main():
    tracker = ProgressTracker()

    # Step 1: Find and rename video to video.mp4
    print("Searching for video file...")
    if not find_and_convert_video():
        return

    video_path = "video.mp4"
    audio_path = "audio.wav"

    # Step 2: Extract audio
    tracker.start_stage("Extracting audio")
    extract_audio(video_path, audio_path)
    tracker.finish_stage()

    # Step 3: Transcribe audio
    tracker.start_stage("Transcribing audio")
    segments = transcribe_audio(audio_path)
    tracker.finish_stage()

    if not segments:
        print("No transcription available.")
        return

    print(f"Transcription complete. {len(segments)} segments found.")

    # Step 4: Search for trigger phrases and build JSON output
    matches = find_trigger_segments(segments)
    if not matches:
        print("No trigger phrases found in transcript.")
        tracker.finish_all()
        return

    # Step 5: Write results to JSON file
    output_path = "timestamps.json"
    with open(output_path, "w") as f:
        json.dump(matches, f, indent=4)
    print(f"\nDetected {len(matches)} voiceline(s). Saved to {output_path}")

    # Step 6: Delete the original video and audio files
    delete_file(video_path)
    delete_file(audio_path)

    tracker.finish_all()


if __name__ == "__main__":
    main()
