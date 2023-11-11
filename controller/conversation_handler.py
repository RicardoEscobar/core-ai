"""This module contains the function that truncates a conversation when the conversation file is too large. When the maximum token length is reached, the conversation is truncated and the conversation is saved to a file."""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))

from pathlib import Path
from typing import List, Dict, Union
import logging

from controller.get_token_count import get_token_count
from controller.create_logger import create_logger
from controller.get_conversation_text import get_conversation_text


# Create a logger instance
module_logger = create_logger(
    logger_name="controller.conversation_handler",
    logger_filename="conversation_handler.log",
    log_directory="logs",
    console_logging=False,
    console_log_level=logging.INFO,
)

def truncate_conversation(conversation: Dict, token_threshold: int) -> Dict:
    """Given a conversation, remove the number of tokens from the conversation.
    Args:
        conversation (Dict): A conversation.
        set_tokens (int): The number of tokens to be used as threshold.
    Returns:
        Dict: A conversation with the tokens removed.
    """
    # if "old_messages" does not exist, then create it.
    if "old_messages" not in conversation:
        conversation["old_messages"] = list()

    # Get the conversation text.
    conversation_text = get_conversation_text(conversation)

    # Get the tokens.
    token_length = get_token_count(conversation_text)

    # Loop until the number of tokens to remove is less than the token length.
    index = 0
    while token_length > token_threshold:
        # Move the message to "old_messages" if the role is not "system".
        try:
            if conversation["messages"][index]["role"] != "system":
                conversation["old_messages"].append(conversation["messages"][index])
                del conversation["messages"][index]
        except IndexError as error:
            print(error)
            print("The conversation is too short.")
            break

        # Recount the number of tokens.
        conversation_text = get_conversation_text(conversation)
        token_length = get_token_count(conversation_text)
        print(f"Token length: {token_length} | token threshold: {token_threshold}")
        index += 1

    return conversation


def truncate_conversation_persona(persona: Dict[str, list]) -> Dict[str, list]:
    """Given a persona (Dict), move the oldest half of the conversation into persona["old_messages"] to handle the token limit.
    Args:
        persona (Dict): A persona.
    Returns:
        Dict: A persona with the tokens removed.
    """

    # Get the conversation.
    messages = persona["messages"]

    # If persona["old_messages"] does not exist, then create it.
    if "old_messages" not in persona:
        persona["old_messages"] = list()

    # Move half of the conversation to "old_messages".
    messages_length = len(messages)
    for _ in range(messages_length // 2):
        persona["old_messages"].append(messages[0])
        del persona["messages"][0]

    return persona


if __name__ == "__main__":
    persona_dict = {
        "messages": [
            {"role": "system", "content": "You are an AI asistant."},
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "How are you?"},
            {"role": "user", "content": "I'm fine"},
            {"role": "assistant", "content": "Goodbye"},
            {"role": "system", "content": "Goodbye"},
        ]
    }
    print(f"Conversation:\n{get_conversation_text(persona_dict)}\n")
    persona_dict = truncate_conversation_persona(persona_dict)
    print(f"Truncated conversation:\n{get_conversation_text(persona_dict)}\n")
    print(f"Old messages:\n{persona_dict['old_messages']}\n")
