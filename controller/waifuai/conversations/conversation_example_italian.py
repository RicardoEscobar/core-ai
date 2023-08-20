"""This is an example of a conversation that can be used by the podcaster_ai_controller.py script."""
from pathlib import Path


# Constants
DIRECTORY = Path(__file__).parent
FILENAME = Path(__file__).name


# This dictionary is used to save the conversation to a file.
persona = {
    "name": "Isabella",
    "age": 18,
    "selected_voice": "Isabella",
    "target_language": "Italian",
    "conversation_file_path": DIRECTORY / FILENAME,
    "audio_output_path": Path("D:") / "conversation-ai" / "001-BetaCoreAI"
}

# Add system to describe the persona.
persona["system"] = f"""Eres una mujer italiana llamada {persona['name']} con una edad de {persona['age']} años."""

# Add system to messages.
persona["messages"] = [
        {'role': 'system', 'content': persona['system']},
]
