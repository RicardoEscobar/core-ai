"""
This module is used to record audio from the microphone and save it to a file.
Then that file is used to convert the audio to text.
Then that text is used to prompt OpenAI's GPT-3.5-Turbo API to generate a response.
Finally, that response is converted to audio and played back to the user.
"""
from pathlib import Path
from datetime import datetime
import openai
from controller.conversation import detect_audio
from controller.conversation import transcribe_audio
from controller.conversation import speech_synthesis
from controller.conversation.speech_synthesis import get_speech_synthesizer
from controller.conversation.speech_synthesis import speak_text
from controller.conversation.completion_create import generate_message
from controller.conversation.completion_create import get_answer
from controller.conversation.completion_create import save_conversation
from controller.conversation.conversations.tsundere_ai_conversation import SYSTEM
from controller.conversation.conversations.tsundere_ai_conversation import MESSAGES
from controller.conversation.load_openai import load_openai


def generate_audio_file_path() -> Path:
    """Generate a file path for the audio file.

    Returns:
        Path: The file path for the audio file.
    """
    # How to put the timestamp into a file name?
    # https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    audio_file_path = Path(__file__).parent / f"prompt_{timestamp}.wav"
    return audio_file_path


def main():
    # Loop until the user says "bye"
    while True:
        # Load the OpenAI API key
        load_openai()

        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate")
        audio_file_path = str(generate_audio_file_path())
        detect_audio.record_to_file(audio_file_path)
        print(f"done - result written to {audio_file_path}")

        # Step 2: Convert the audio to text.
        transcribed_prompt = transcribe_audio.transcribe(audio_file_path)
        print(f"Transcribed prompt: {transcribed_prompt}")

        # Step 3: Prompt OpenAI's GPT-3.5-Turbo API to generate a response.    
        # Save the user input to the messages list
        MESSAGES.append(generate_message("user", transcribed_prompt))

        # Save the response to the messages list
        response = get_answer(MESSAGES)['choices'][0]['message']['content']
        MESSAGES.append(generate_message("assistant", response))
        print(f'\nAssistant: {response}')

        # Save the MESSAGES list to the tsundere_ai_conversation.py file.
        conversation_path = Path(__file__).parent / "conversations" / "tsundere_ai_conversation.py"
        save_conversation(MESSAGES, SYSTEM, str(conversation_path))

        # Step 4: Convert the response to audio and play it back to the user.
        # Constants for speech synthesis configuration
        SELECTED_VOICE = 'Tania'

        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(SELECTED_VOICE)

        # Speak the text
        speak_text(speech_synthesizer, response)

        # If the transcribed_prompt contains "bye." then break out of the loop
        if transcribed_prompt.lower().find("bye.") != -1:
            break

if __name__ == '__main__':
    main()