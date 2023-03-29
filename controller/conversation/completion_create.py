# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
from typing import List, Dict
from pathlib import Path
import openai
from controller.conversation.conversations.tsundere_ai_conversation import SYSTEM
from controller.conversation.conversations.tsundere_ai_conversation import MESSAGES
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

def get_answer(messages: List = None) -> str:
    answer = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    )
    return answer

def save_conversation(conversation: List, system: str, conversation_path: str, selected_voice: str = 'Salome'):
    with open(Path(conversation_path), mode="w", encoding='utf-8') as file:
        file.write(f'SELECTED_VOICE = """{system}"""\n')
        file.write(f'SYSTEM = """{system}"""\n')
        file.write(f'MESSAGES = {conversation}\n')

def main():
    # Loop until the user says "bye"
    while True:        
        # Prompt the user for input
        user_input = input("\nUser: ")

        # Save the user input to the messages list
        MESSAGES.append(generate_message("user", user_input))

        response = get_answer(MESSAGES)['choices'][0]['message']['content']
        print(f'\nAssistant: {response}')

        # Save the response to the messages list
        MESSAGES.append(generate_message("assistant", response))

        # If the user says "bye" then break out of the loop
        if user_input == "bye":
            break

    
    # Save the MESSAGES list to the tsundere_ai_conversation.py file.
    conversation_path = Path(__file__).parent / "conversations" / "tsundere_ai_conversation.py"
    save_conversation(MESSAGES, SYSTEM, str(conversation_path))
    

if __name__ == "__main__":
    main()