import os

SUPPORTED_FORMATS = [".mp4", ".mov", ".avi", ".mkv"]


def find_video_file():
    """
    Searches the current folder for any supported video file.
    If video.mp4 already exists, uses it directly.

    Returns:
        str: The filename of the video to use, or None if none found.
    """
    # If video.mp4 already exists, just use it
    if os.path.exists("video.mp4"):
        print("Found existing video.mp4, using it directly.")
        return "video.mp4"

    found = []
    for file in os.listdir(""):
        if os.path.splitext(file)[1].lower() in SUPPORTED_FORMATS:
            found.append(file)

    if len(found) == 0:
        print("No video files found in this folder. Please add an mp4, mov, avi, or mkv file.")
        return None
    elif len(found) == 1:
        print(f"Found video: '{found[0]}'")
        return found[0]
    else:
        print("Multiple video files found:")
        for i, f in enumerate(found):
            print(f"  [{i + 1}] {f}")
        while True:
            choice = input("Enter the number of the video to use: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(found):
                return found[int(choice) - 1]
            print("Invalid choice, please try again.")


def convert_to_standard(output_filename="video.mp4"):
    """
    Finds a video file in the current folder and renames it to video.mp4.
    If video.mp4 already exists, skips renaming.

    Returns:
        bool: True if successful, False otherwise.
    """
    input_filename = find_video_file()
    if not input_filename:
        return False

    if input_filename == output_filename:
        return True  # Already named correctly, nothing to do

    os.rename(input_filename, output_filename)
    print(f"'{input_filename}' renamed to '{output_filename}'")
    return True


if __name__ == "__main__":
    convert_to_standard()