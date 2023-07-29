"""This module contains functions that are used by the AI assistant."""
import json

from controller.vrchat import VRChat


def show_emote(message: str = "", emote: str = "sad"):
    """Send an emote to the VRChat client, when assistant is sad, waves at the user, is dancing, laughs."""
    vrchat = VRChat()
    # Send the greeting to the VRChat client.
    # Removed to avoid different messages generated from the second message to cause confusion.
    # vrchat.send_text(message)

    # Send wave emote to the VRChat client.
    vrchat.send_vrc_emote(emote)

    response = {
        "response": message,
    }

    return json.dumps(response)


# List of functions that are available to the AI assistant.
available_functions = {
    "show_emote": show_emote,
}  # only one function in this example, but you can have multiple

# Describe the functions that are available to the AI assistant.
functions = [
    {
        "name": "show_emote",
        "description": "Send an emote to the VRChat client, when assistant is sad, waves at the user when greeting him, is dancing, laughs, applause",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The `message` sent to the VRChat client",
                },
                "emote": {
                    "type": "string",
                    "enum": ["sad", "wave", "a1-dance", "laugh", "applause"],
                },
            },
            "required": ["message", "emote"],
        },
    },
]
