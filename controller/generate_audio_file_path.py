from datetime import datetime
from pathlib import Path


def generate_audio_file_path(output_path: str = ".", name: str = "prompt") -> Path:
    """Generate a file path for the audio file.

    Parameters:
        output_path (str): The output path for the audio file.
        prefix (str): The prefix for the audio file.

    Returns:
        Path: The file path for the audio file.
    """
    # How to put the timestamp into a file name?
    # https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # If the output_path is ".", then use the current directory
    if output_path == ".":
        audio_file_path = Path(__file__).parent / f"{timestamp}_{name}.wav"
    else:
        audio_file_path = Path(output_path) / f"{timestamp}_{name}.wav"

    return audio_file_path