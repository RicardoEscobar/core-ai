from typing import Dict

def get_conversation_text(persona: Dict) -> str:
    """Given a conversation, return the text of the conversation.
    Args:
        conversation (Dict): A conversation.
    Returns:
        str: The text of the conversation.
    """
    # Get the conversation text.
    conversation_text = ""

    for message in persona["messages"]:
        conversation_text += message["role"] + ": " + message["content"] + "\n"

    return conversation_text