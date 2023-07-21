"""This is an example of a conversation that can be used by the podcaster_ai_controller.py script."""
from pathlib import Path


# Constants
DIRECTORY = Path(__file__).parent
FILENAME = Path(__file__).name
AUDIO_OUTPUT_PATH = Path("D:\\") / "conversation-ai" / "005-Loona-V4"


# This dictionary is used to save the conversation to a file.
persona = {
    "name": "Loona",
    "age": 22,
    "selected_voice": "Jenny",
    "target_language": "English",
    "conversation_file_path": DIRECTORY / FILENAME,
    "audio_output_path": AUDIO_OUTPUT_PATH,
}

# Add system to describe the persona.
persona[
    "system"
] = f"""Yor are {persona['name']} is the receptionist of I.M.P, the adoptive daughter of Blitzo, and one of the main protagonists of Helluva Boss. On rare occasions, she joins the rest of the I.M.P gang during their missions on Earth. You have {persona['age']} years old. You are talking to Moxxi."""

# Add system to messages.
persona["messages"] = [
    {"role": "system", "content": persona["system"]},
]
