"""This module contains the function that truncates a conversation when the conversation file is too large. When the maximum token length is reached, the conversation is truncated and the conversation is saved to a file."""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))

from pathlib import Path

from controller.get_token_count import get_token_count


def get_conversation_text(conversation: dict) -> str:
    """Given a conversation, return the text of the conversation.
    Args:
        conversation (dict): A conversation.
    Returns:
        str: The text of the conversation.
    """
    # Get the conversation text.
    conversation_text = ""

    for message in conversation["messages"]:
        conversation_text += message["role"] + ": " + message["content"] + "\n"

    return conversation_text

def truncate_conversation(conversation: dict, token_threshold: int) -> dict:
    """Given a conversation, remove the number of tokens from the conversation.
    Args:
        conversation (dict): A conversation.
        set_tokens (int): The number of tokens to be used as threshold.
    Returns:
        dict: A conversation with the tokens removed.
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


if __name__ == "__main__":
    conversation = {"messages": [{"role": "system", "content": "You are an AI asistant."},
                                 {"role": "user", "content": "Hi"},
                                 {"role": "assistant", "content": "How are you?"},
                                 {"role": "user", "content": "I'm fine"},
                                 {"role": "assistant", "content": "Goodbye"}]}
    print(f"Conversation:\n{get_conversation_text(conversation)}\n")
    conversation = truncate_conversation(conversation, 2000)
    print(f"Conversation:\n{get_conversation_text(conversation)}\n")