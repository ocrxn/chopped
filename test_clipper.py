from clipper import cut_clip

video_path = "uploads/game_video.mp4"
output_path = "clips/test_clip.mp4"

cut_clip(video_path=video_path, start_time=4, duration=8, output_path=output_path)

print("Finished. Check the clips folder")