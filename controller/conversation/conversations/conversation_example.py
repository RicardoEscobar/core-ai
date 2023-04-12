"""This is an example of a conversation that can be used by the podcaster_ai_controller.py script."""
from pathlib import Path


# Constants
DIRECTORY = Path(__file__).parent
FILENAME = Path(__file__).name


# This dictionary is used to save the conversation to a file.
persona = {
    "name": "Larissa",
    "age": 18,
    "selected_voice": "Larissa",
    "target_language": "English",
    "conversation_file_path": DIRECTORY / FILENAME,
    "audio_output_path": Path("D:") / "podcaster-ai" / "MenteDoble" / "008-Larissa",
}

# Add system to describe the persona.
persona["system"] = f"""Eres {persona['name']} ({persona['age']}) Tu eres una mujer tsundere."""

# Add system to messages.
persona["messages"] = [
        {'role': 'system', 'content': persona['system']},
]
