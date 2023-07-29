# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
from typing import List, Dict
from pathlib import Path
import json

import openai

from controller.conversation.load_openai import load_openai
from controller.create_logger import create_logger
from controller.ai_functions import available_functions
from controller.ai_functions import functions

# Load the OpenAI API key
load_openai()
# Create logger
module_logger = create_logger(
    logger_name=__name__,
    logger_filename="completion_create.log",
    log_directory="logs",
    add_date_to_filename=False,
)

# Constants
MODEL_USED = "gpt-4-0613"  # "gpt-3.5-turbo-0613"


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
    # create a copy of the messages list
    new_messages = messages.copy()

    try:
        # TODO Clean first_response from the function call <OpenAIObject chat.completion id=chatcmpl-7hT6Eb2ILdAssFb1YCBkF7kgjrBvf at 0x1858658dd90> JSON: {...
        first_response = openai.ChatCompletion.create(
            model=MODEL_USED,
            messages=new_messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
            temperature=1.0,
            max_tokens=200,  # 8,192 tokens is the max for GPT-4
            # stop=["\n\n", "Link:", "system:"],
        )
        module_logger.info(
            "Before processing: first_response = %s", repr(first_response)
        )
    except openai.error.InvalidRequestError as error:
        print(f"Error: {error}")
        return None
    else:
        module_logger.info("Error ==> %s", first_response["choices"][0]["message"])

        # Get the response message
        response_message = first_response["choices"][0]["message"]

        # Check if GPT wanted to call a function
        if response_message.get("function_call"):
            module_logger.info("Function call: %s", response_message["function_call"])

            # Call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            function_name = response_message["function_call"]["name"]
            fuction_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = fuction_to_call(**function_args)

            module_logger.info(
                "Before Send the info on the function call and function response to GPT response_message = %s",
                repr(response_message),
            )

            # Send the info on the function call and function response to GPT
            # extend conversation with assistant's reply
            new_messages.append(response_message)

            # convert function response to unicode
            function_response_unicode = bytes(
                function_response,
                "utf-8",
            ).decode("unicode-escape")

            # Create a new message with the function response
            function_response_dict = {
                "role": "function",
                "name": function_name,
                "content": function_response_unicode,
            }

            # extend conversation with function response
            new_messages.append(function_response_dict)
            messages.append(function_response_dict)

            second_response = openai.ChatCompletion.create(
                model=MODEL_USED,  # "gpt-4-0613", "gpt-3.5-turbo-0613",
                messages=new_messages,
            )  # get a new response from GPT where it can see the function response
            module_logger.info("second_response = %s", repr(second_response))

            return second_response
        else:
            return first_response


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
