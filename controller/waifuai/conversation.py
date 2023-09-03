"""
This module is used to record audio from the microphone and save it to a file.
Then that file is used to convert the audio to text.
Then that text is used to prompt OpenAI's GPT-3.5-Turbo API to generate a response.
Finally, that response is converted to audio and played back to the user.
"""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent.parent
    sys.path.append(str(root_folder))

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Union
import threading
import pickle

import openai
from elevenlabs.api import Voice, VoiceSettings

import controller.waifuai.detect_audio as detect_audio
import controller.waifuai.transcribe_audio as transcribe_audio
from controller.waifuai.speech_synthesis import get_speech_synthesizer
from controller.waifuai.speech_synthesis import speak_text_into_file
from controller.waifuai.completion_create import generate_message
from controller.waifuai.completion_create import get_response
from controller.llmchain import get_response_unfiltered
from controller.waifuai.completion_create import save_conversation
from controller.waifuai.play_audio import play_audio
from controller.waifuai.play_audio import get_wav_duration
from controller.waifuai.conversations.conversation_example import persona
from controller.load_openai import load_openai
from controller.natural_voice import generate_multilingual
from controller.code_filter import CodeFilter
from controller.vrchat import VRChat


def create_folder(folder_path: str = ".") -> Path:
    """Create a folder if it does not already exist.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        Path: The path to the folder.
    """
    if folder_path == ".":
        returned_folder_path = Path(__file__).parent / "conversations"
    else:
        returned_folder_path = Path(folder_path)

    if not returned_folder_path.exists():
        returned_folder_path.mkdir(parents=True, exist_ok=True)

    return returned_folder_path


def generate_audio_file_path(output_path: str = ".", name: str = "prompt") -> Path:
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

    # If the output_path is ".", then use the current directory
    if output_path == ".":
        audio_file_path = Path(__file__).parent / f"{timestamp}_{name}.wav"
    else:
        audio_file_path = Path(output_path) / f"{timestamp}_{name}.wav"

    return audio_file_path


def translator(selected_voice: str = "Jenny", target_language: str = "English"):
    # Loop until the user says "bye"
    while True:
        # Load the OpenAI API key
        load_openai()

        # Create the output folder if it doesn't exist
        output_folder = create_folder(persona["audio_output_path"])

        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate")
        audio_file_path = str(
            generate_audio_file_path(output_folder, "JorgeEscobar_human")
        )
        detect_audio.record_to_file(audio_file_path)
        print(f"done - result written to {audio_file_path}")

        # Step 2: Translate the audio to target language.
        transcribed_prompt = transcribe_audio.transcribe(audio_file_path)

        # Add translation instructions to the prompt
        transcribed_prompt = f'{transcribed_prompt}"'
        print(f"Transcribed prompt: {transcribed_prompt}")

        # Step 3: Prompt OpenAI's GPT-3.5-Turbo API to generate a response.
        # Save the user input to the persona["messages"] list
        persona["messages"].append(generate_message("user", transcribed_prompt))

        # Save the response to the persona["messages"] list
        response = get_response(persona["messages"])
        persona["messages"].append(generate_message("assistant", response))
        print(f"\nAssistant: {response}")

        # Save the persona["messages"] list to the conversation file.
        conversation_path = (
            Path(__file__).parent / "conversations" / persona["conversation_file_path"]
        )
        save_conversation(persona)

        # Step 4: Convert the response to audio and play it back to the user.
        # Get a speech synthesizer
        # speech_synthesizer = get_speech_synthesizer(selected_voice)
        assistant_audio_file_path = str(
            generate_audio_file_path(output_folder, persona["name"])
        )

        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(
            selected_voice, assistant_audio_file_path
        )

        # Speak the text
        speak_text_into_file(speech_synthesizer, response)
        play_audio(assistant_audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        if transcribed_prompt.lower().find("bye.") != -1:
            break


def conversation(
    selected_voice: str = persona["selected_voice"],
    is_filtered: bool = True,
    natural_voice: Union[Voice, str] = None,
):
    # Load the OpenAI API key
    load_openai()

    # Create the output folder if it doesn't exist
    output_folder = create_folder(persona["audio_output_path"])

    # Loop until the user says "bye"
    while True:
        # Preparation: Generate the file paths for the audio files.
        human_audio_file_path = str(
            generate_audio_file_path(output_folder, "JorgeEscobar_human")
        )

        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate...\n")
        detect_audio.record_to_file(human_audio_file_path)
        print(f"done - result written to {human_audio_file_path}\n")

        # Step 2: Convert the audio to text.
        transcribed_prompt = transcribe_audio.transcribe(human_audio_file_path)
        print(f"\033[31mUser:\033[0m \033[33m{transcribed_prompt}\033[0m\n")

        # Step 3: Prompt OpenAI's GPT-3.5-Turbo API to generate a response.
        # Save the user input to the persona["messages"] list
        persona["messages"].append(generate_message("user", transcribed_prompt))

        # if is_filtered is True, then filter the response
        if is_filtered:
            # Save the filtered response to the persona["messages"] list
            response = get_response(persona["messages"])
        else:
            # Save the unfiltered response to the persona["messages"] list
            response = get_response_unfiltered(human_input=transcribed_prompt)

        # Save the response to the persona["messages"] list
        persona["messages"].append(generate_message("assistant", response))

        # If selected_voice is None, then use the default voice
        save_conversation(persona)

        # Step 4: Convert the response to audio and play it back to the user.
        # Generate the file path for the audio file, removing spaces from the persona["name"].
        assistant_audio_file_path = str(
            generate_audio_file_path(output_folder, persona["name"].replace(" ", "_"))
        )

        # Clean the response from code blocks before synthesizing the audio.
        # response = CodeFilter(text=response).filtered_str # TODO replace, refactor, or remove this line.

        # If natural_voice is None, then use the default voice, else use the natural voice.
        if natural_voice is None:
            # Get a speech synthesizer
            speech_synthesizer = get_speech_synthesizer(
                selected_voice, assistant_audio_file_path
            )

            # Generate the audio file
            speak_text_into_file(speech_synthesizer, response)

        else:
            # Generates the audio file using the natural voice
            generate_multilingual(response, natural_voice, assistant_audio_file_path)

        # Speak the text
        print(assistant_audio_file_path)

        # Calculate the duration of the audio file
        duration = get_wav_duration(assistant_audio_file_path)

        # Create a VRChat instance
        vrchat = VRChat()

        # Split the response into chunks of 144 characters
        response_chunks = vrchat.split_string(response)

        # Send the response to VRChat
        vrchat.send_text_list(response_chunks, duration)
        play_audio(assistant_audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        if transcribed_prompt.lower().find("bye") != -1:
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

        # Create the output folder if it doesn't exist
        output_folder = create_folder(persona["audio_output_path"])

        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate")
        audio_file_path = str(
            generate_audio_file_path(output_folder, "JorgeEscobar_human")
        )
        detect_audio.record_to_file(audio_file_path)
        print(f"done - result written to {audio_file_path}")

        # Step 2: Convert the audio to text.
        transcribed_prompt = transcribe_audio.transcribe(audio_file_path)
        print(f"Transcribed prompt: {transcribed_prompt}")

        # Step 3: Convert the response to audio and play it back to the user.
        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(selected_voice, audio_file_path)

        # Speak the text
        speak_text_into_file(speech_synthesizer, transcribed_prompt)
        play_audio(audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        if transcribed_prompt.lower().find("bye.") != -1:
            break


def main():
    # dubbing(persona["selected_voice"])
    female_natural_voice = Voice(
        voice_id="chQ8GR2cY20KeFjeSaXI",
        name="[ElevenVoices] Hailey - American Female Teen",
        category="generated",
        description="",
        labels={
            "accent": "american",
            "age": "young",
            "voicefrom": "ElevenVoices",
            "gender": "female",
        },
        samples=None,
        settings=VoiceSettings(stability=0.5, similarity_boost=0.75),
        design=None,
        preview_url="https://storage.googleapis.com/eleven-public-prod/PyUBusauIUbpupKTM31Yp4fHtgd2/voices/OgTivnXy9Bsc96AcZaQz/44dc6d49-cd44-4aad-a453-73a12c215702.mp3",
    )

    male_natural_voice = Voice(
        voice_id="64EnPc3cxmsX0tj6z2lD",
        name="Deep resonant male voice; confident, light British accent, sexy",
        category="generated",
        description="",
        labels={"accent": "british", "age": "middle_aged", "gender": "male"},
        samples=None,
        settings=VoiceSettings(stability=0.5, similarity_boost=0.75),
        design=None,
        preview_url="https://storage.googleapis.com/eleven-public-prod/udmG0I9oKegHHyrU3sEvatdvG2p1/voices/qA6nnGfIRBPIRDeNkPCa/725ee1eb-06f4-4521-9e49-1511cb3a5fb7.mp3",
    )

    loona_natural_voice = Voice(
        voice_id="07If6JkaNiXuzSTEgKuj",
        name="Christina - Trained on over 900 characters with emotional dialogue",
        category="generated",
        description="",
        labels={"accent": "american", "age": "young", "gender": "female"},
        samples=None,
        settings=VoiceSettings(stability=0.5, similarity_boost=0.75),
        design=None,
        preview_url="https://storage.googleapis.com/eleven-public-prod/U1Rx6ByQzXTKXc5wPxu4fXvSRqO2/voices/07If6JkaNiXuzSTEgKuj/c973d3e5-89f1-43e8-861d-89ef866ce41f.mp3",
    )

    # Run the conversation
    conversation(
        persona["selected_voice"],  # The default voice is used
        is_filtered=True,  # Set to False to enable NSFW content
        natural_voice=None,  # Set to None to use the default voice
    )


if __name__ == "__main__":
    main()
