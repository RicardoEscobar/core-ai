# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
from typing import List, Dict
from pathlib import Path
import openai
from controller.conversation.load_openai import load_openai

# Load the OpenAI API key
load_openai()


def generate_message(role: str, content: str) -> Dict:
    """
    Generate a message for the OpenAI API.

    Args:
        role (str): The role of the message either "system", "user", or "assistant".
        content (str): The content of the message.
    """
    message = {"role": role, "content": content}
    return message


def get_response(messages: List) -> str:
    """
    Get the answer from the OpenAI API.

    Args:
        messages (List): The messages to send to the OpenAI API.

    Returns:
        str: The answer from the OpenAI API.
    """
    try:
        answer = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            temperature=1.0,
            max_tokens=200, # 8,192 tokens is the max for GPT-4
            #stop=["\n\n", "Link:", "system:"],
        )
    except openai.error.InvalidRequestError as error:
        print(f"Error: {error}")
        return None
    else:
        return answer


def save_conversation(persona: Dict):
    # Save the conversation to the conversation file.
    with open(persona["conversation_file_path"], mode="w", encoding="utf-8") as file:
        file.write(
            '"""This is an example of a conversation that can be used by the podcaster_ai_controller.py script."""\n'
        )
        file.write(
            f"""from pathlib import Path, WindowsPath, PosixPath, PureWindowsPath, PurePosixPath, PurePath

# This dictionary is used to save the conversation to a file.
persona  = {repr(persona)}\n"""
        )


def main():
    # # Loop until the user says "bye"
    # while True:
    #     # Prompt the user for input
    #     user_input = input("\nUser: ")

    #     # Save the user input to the messages list
    #     MESSAGES.append(generate_message("user", user_input))

    #     response = get_answer(MESSAGES)["choices"][0]["message"]["content"]
    #     print(f"\nAssistant: {response}")

    #     # Save the response to the messages list
    #     MESSAGES.append(generate_message("assistant", response))

    #     # If the user says "bye" then break out of the loop
    #     if user_input == "bye":
    #         break

    # Save the MESSAGES list to the tsundere_ai_conversation.py file.
    # conversation_path = Path(__file__).parent / "conversations" / "tsundere_ai_conversation.py"
    # save_conversation()
    pass


if __name__ == "__main__":
    main()
