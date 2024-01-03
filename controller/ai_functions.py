"""This module contains functions that are used by the AI assistant."""
import json

from controller.vrchat import VRChat
from controller.youtube.youtube_search import ai_youtube_search
from controller.vision.eyes import Eyes


def show_emote(message: str = "", emote: str = "sad", prompt: str = ""):
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
    "ai_youtube_search": ai_youtube_search,
    "take_picture_and_process": Eyes.take_picture_and_process,
}  # only one function in this example, but you can have multiple

# Describe the functions that are available to the AI assistant.
tools = [
    {
        "type": "function",
        "function": {
            "name": "take_picture_and_process",
            "description": "Use this when asked to see something or someone inside VRChat and talk about it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to use.",
                    }
                },
                "required": ["prompt"],
            },
        },
    },
    {
        "type": "function",
        "function": {
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
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to use.",
                    },
                },
                "required": ["message", "emote"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ai_youtube_search",
            "description": "Search for a video on YouTube and return the transcript.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to search for on YouTube",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "The directory to save the transcript to",
                    },
                    "max_videos": {
                        "type": "string",
                        "description": "The maximum number of videos to summarize",
                    },
                    "max_tokens": {
                        "type": "string",
                        "description": "The maximum number of tokens for the AI model to use for each video",
                    },
                },
                "required": ["prompt"],
            },
        },
    },
]
