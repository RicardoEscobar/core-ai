"""
This module is used to record audio from the microphone and save it to a file.
Then that file is used to convert the audio to text.
Then that text is used to prompt OpenAI's GPT-3.5-Turbo API to generate a response.
Finally, that response is converted to audio and played back to the user.
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import openai
from controller.conversation import detect_audio
from controller.conversation import transcribe_audio
from controller.conversation.speech_synthesis import get_speech_synthesizer
from controller.conversation.speech_synthesis import speak_text
from controller.conversation.completion_create import generate_message
from controller.conversation.completion_create import get_answer
from controller.conversation.completion_create import save_conversation
from controller.conversation.play_audio import play_audio
from controller.conversation.conversations.conversation_example import persona
from controller.conversation.load_openai import load_openai


def create_folder(folder_path: str = None) -> Path:
    """Create a folder if it does not already exist.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        Path: The path to the folder.
    """
    if folder_path is None:
        folder_path = Path(__file__).parent / "conversations"
    else:
        folder_path = Path(folder_path)

    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
    
    return folder_path

def generate_audio_file_path(output_path: str = None, name: str = 'prompt') -> Path:
    """Generate a file path for the audio file.

    Parameters:
        output_path (str): The output path for the audio file.
        prefix (str): The prefix for the audio file.

    Returns:
        Path: The file path for the audio file.
    """
    # How to put the timestamp into a file name?
    # https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # If the output_path is None, then use the current directory
    if output_path is None:
        audio_file_path = Path(__file__).parent / f"{timestamp}_{name}.wav"
    else:
        audio_file_path = Path(output_path) / f"{timestamp}_{name}.wav"

    return audio_file_path

def translator(selected_voice: str = "Jenny", target_language: str = "English"):
    # Loop until the user says "bye"
    while True:
        # Load the OpenAI API key
        load_openai()

        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate")
        audio_file_path = str(generate_audio_file_path())
        detect_audio.record_to_file(audio_file_path)
        print(f"done - result written to {audio_file_path}")

        # Step 2: Translate the audio to target language.
        transcribed_prompt = transcribe_audio.transcribe(audio_file_path)
        
        # Add translation instructions to the prompt
        transcribed_prompt = f"Translate to {target_language}: {transcribed_prompt}"
        print(f"Transcribed prompt: {transcribed_prompt}")

        # Step 3: Prompt OpenAI's GPT-3.5-Turbo API to generate a response.
        # Save the user input to the persona["messages"] list
        persona["messages"].append(generate_message("user", transcribed_prompt))

        # Save the response to the persona["messages"] list
        response = get_answer(persona["messages"])['choices'][0]['message']['content']
        persona["messages"].append(generate_message("assistant", response))
        print(f'\nAssistant: {response}')

        # Save the persona["messages"] list to the conversation file.
        conversation_path = Path(__file__).parent / "conversations" / persona["conversation_file_path"]
        save_conversation(persona)

        # Step 4: Convert the response to audio and play it back to the user.
        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(selected_voice)

        # Speak the text
        speak_text(speech_synthesizer, response)

        # If the transcribed_prompt contains "bye." then break out of the loop
        if transcribed_prompt.lower().find("bye.") != -1:
            break

def conversation(selected_voice: str = persona["selected_voice"]):
    # Load the OpenAI API key
    load_openai()

    # Select an output path for the audio files.
    output_folder = create_folder(persona["audio_output_path"])

    # Create the output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Loop until the user says "bye"
    while True:
        # Preparation: Generate the file paths for the audio files.
        human_audio_file_path = str(generate_audio_file_path(output_folder, "JorgeEscobar_human"))
        
        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate...\n")
        detect_audio.record_to_file(human_audio_file_path)
        print(f"done - result written to {human_audio_file_path}\n")

        # Step 2: Convert the audio to text.
        transcribed_prompt = transcribe_audio.transcribe(human_audio_file_path)
        print(f"Transcribed prompt: {transcribed_prompt}\n")

        # Step 3: Prompt OpenAI's GPT-3.5-Turbo API to generate a response.
        # Save the user input to the persona["messages"] list
        persona["messages"].append(generate_message("user", transcribed_prompt))

        # Save the response to the persona["messages"] list
        response = get_answer(persona["messages"])['choices'][0]['message']['content']
        persona["messages"].append(generate_message("assistant", response))
        
        # If selected_voice is None, then use the default voice
        save_conversation(persona)

        # Step 4: Convert the response to audio and play it back to the user.        
        # Generate the file path for the audio file
        assistant_audio_file_path = str(generate_audio_file_path(output_folder, persona["name"]))
        
        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(selected_voice, assistant_audio_file_path)

        # Speak the text
        speak_text(speech_synthesizer, response)
        play_audio(assistant_audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        if transcribed_prompt.lower().find("bye.") != -1:
            break

def dubbing(selected_voice: str = "Juan"):
    """
    This function is used to dubbing the audio from the microphone and save it to a file.
    Then that file is used to convert the audio to text.
    Finally, that text is converted to audio and played back to the user.
    """
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

        # Step 3: Convert the response to audio and play it back to the user.
        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(selected_voice)

        # Speak the text
        speak_text(speech_synthesizer, transcribed_prompt)

        # If the transcribed_prompt contains "bye." then break out of the loop
        if transcribed_prompt.lower().find("bye.") != -1:
            break

def main():
    conversation()

if __name__ == '__main__':
    main()