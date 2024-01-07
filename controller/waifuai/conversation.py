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
from typing import Dict, List, Union, Tuple
import logging

from elevenlabs.api import Voice, VoiceSettings, VoiceSample
import openai
import traceback

from controller.waifuai.conversations.cecilia import persona
from controller import detect_audio
from controller import transcribe_audio
from controller.speech_synthesis import get_speech_synthesizer, speak_text_into_file
from controller.waifuai.completion_create import (
    generate_message,
    get_response,
    save_conversation,
)
from controller.llmchain import get_response_unfiltered
from controller.play_audio import play_audio, get_audio_duration
from controller.load_openai import load_openai
from controller.natural_voice import generate_multilingual
from controller.vrchat import VRChat
from controller.create_folder import create_folder
from controller.get_audio_filepath import get_audio_filepath
from controller.conversation_handler import truncate_conversation
from controller.stream_completion import StreamCompletion
from controller.create_logger import create_logger
from controller.vision.eyes import Eyes
from controller.transcribe_audio import language_codes
from controller.ai_functions import ai_available_functions, tools
from controller.voices_elevenlabs import get_voice_by_id


# Create a logger
logger = create_logger(
    logger_name="controller.waifuai.conversation",
    logger_filename="conversation.log",
    console_logging=True,
    console_log_level=logging.INFO,
)


def translator(selected_voice: str = "Jenny", target_language: str = "English"):
    # Loop until the user says "bye"
    while True:
        # Load the OpenAI API key
        load_openai()

        # Create the output folder if it doesn't exist
        output_dir = create_folder(persona["audio_output_path"])

        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate")
        audio_file_path = get_audio_filepath(
            output_dir=output_dir, text="JorgeEscobar_human"
        )

        detect_audio.record_to_file(audio_file_path)
        print(f"done - result written to {audio_file_path}")

        # Step 2: Translate the audio to target language.
        target_language = persona["target_language"]
        transcribed_prompt = transcribe_audio.transcribe(
            audio_file_path, language=language_codes[target_language]
        )

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
        assistant_audio_file_path = get_audio_filepath(
            output_dir=output_dir, text=persona["name"]
        )

        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(
            selected_voice, assistant_audio_file_path
        )

        # Speak the text
        speak_text_into_file(speech_synthesizer, response)
        play_audio(assistant_audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        goodbye_words = ["bye", "goodbye", "adíos"]

        if any(word in transcribed_prompt.lower() for word in goodbye_words):
            break


def conversation(
    persona_data: Dict,
    selected_voice: str = persona["selected_voice"],
    is_filtered: bool = True,
    natural_voice: Union[Voice, str] = None,
) -> None:
    """This function is used to record audio from the microphone and save it to a file.
    Then that file is used to convert the audio to text.
    Then that text is used to prompt OpenAI's GPT-3.5-Turbo API to generate a response.
    Finally, that response is converted to audio and played back to the user.

    Args:
        persona_data (Dict): The persona data.
        selected_voice (str, optional): The selected voice. Defaults to persona["selected_voice"].
        is_filtered (bool, optional): Set to False to enable NSFW content. Defaults to True.
        natural_voice (Union[Voice, str], optional): Set to None to use the
        default voice. Defaults to None.
    """
    # gpt-4-vision-preview has a max token length of 128,000. Returns a maximum
    # of 4,096 output tokens.So 128_000 - 4096 = 123_904 as the token threshold.
    TOKEN_THRESHOLD = 123_904

    # Load the OpenAI API key
    load_openai()

    # Create the output folder if it doesn't exist
    print(f"persona = {persona_data['audio_output_path']}")
    output_folder = create_folder(persona_data["audio_output_path"])

    # Loop until the user says "bye"
    while True:
        # Preparation: Generate the file paths for the audio files.
        human_audio_file_path = get_audio_filepath(
            output_dir=output_folder, text="JorgeEscobar_human"
        )

        # Step 1: Record audio from the microphone and save it to a file.
        print("Wait in silence to begin recording; wait in silence to terminate...\n")
        detect_audio.record_to_file(human_audio_file_path)
        print(f"done - result written to {human_audio_file_path}\n")

        # Step 2: Convert the audio to text.
        target_language = persona_data["target_language"]
        transcribed_prompt = transcribe_audio.transcribe(
            human_audio_file_path, language=language_codes[target_language]
        )
        print(f"\033[31mUser:\033[0m \033[33m{transcribed_prompt}\033[0m\n")
        logger.debug("transcribed_prompt = %s", transcribed_prompt)

        # Step 3: Prompt OpenAI's GPT-3.5-Turbo API to generate a response.
        # Save the user input to the persona["messages"] list
        persona_data["messages"].append(generate_message("user", transcribed_prompt))
        logger.info("persona['messages'] = %s", persona_data["messages"])

        # if is_filtered is True, then filter the response
        if is_filtered:
            # Save the filtered response to the persona["messages"] list
            while True:
                try:
                    response = get_response(persona_data["messages"], model="gpt-4")
                except Exception as error:
                    print(error)
                    print("The conversation is too long.")
                    # Truncate the conversation
                    persona_data = truncate_conversation(persona_data, TOKEN_THRESHOLD)
                    continue
                else:
                    break
        else:
            # Save the unfiltered response to the persona["messages"] list
            response = get_response_unfiltered(human_input=transcribed_prompt)

        # Save the response to the persona["messages"] list
        persona_data["messages"].append(generate_message("assistant", response))

        # If selected_voice is None, then use the default voice
        save_conversation(persona_data)

        # Step 4: Convert the response to audio and play it back to the user.
        # Generate the file path for the audio file, removing spaces from the persona["name"].
        assistant_audio_file_path = get_audio_filepath(
            output_dir=output_folder, text=persona_data["name"].replace(" ", "_")
        )

        # Clean the response from code blocks before synthesizing the audio.
        # response = CodeFilter(text=response).filtered_str # TODO replace,
        # refactor, or remove this line.

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

        # Calculate the duration of the audio file
        duration = get_audio_duration(assistant_audio_file_path)

        # Create a VRChat instance
        vrchat = VRChat()

        # Split the response into chunks of 144 characters
        response_chunks = vrchat.split_string(response)

        # Send the response to VRChat
        vrchat.send_text_list(response_chunks, duration)
        play_audio(assistant_audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        goodbye_words = ["bye", "goodbye", "adíos"]

        if any(word in transcribed_prompt.lower() for word in goodbye_words):
            break


def stream_conversation(
    persona_data: Dict,
    gpt_model: str = "gpt-4",
    selected_voice: str = persona["selected_voice"],
    natural_voice: Union[Voice, str] = None,
    voice_model: str = "eleven_turbo_v2",
    is_filtered: bool = True,
    output_dir: str = ".",
    max_tokens: int = 50,
    stop: Union[str, List[str]] = None,
    tools: List[Dict] = None,
    tool_choice: str = "auto",
    available_functions: Dict = None,
    yield_characters: Tuple = None,
):
    """This version of conversation method uses the StreamCompletion class. So it's faster than the conversation method."""

    if stop is None:
        stop = ["Jorge:"]

    if available_functions is None:
        available_functions = persona_data["available_functions"]

    if yield_characters is None:
        yield_characters = (".", "?", "!", "\n", ":", ";")

    # TODO: Replace this with the max token length for the given model,
    # calculate it or get it from openai.api
    TOKEN_THRESHOLD = 4096  # Half of the max token length for GTP-4 (8192 tokens)
    # Load the OpenAI API key
    load_openai()

    # Create a StreamCompletion instance
    stream_completion = StreamCompletion(
        voice=natural_voice,
        voice_model=voice_model,
        persona=persona_data["system"],
        gpt_model=gpt_model,
        temperature=0.9,
        stream_mode=True,
        max_tokens=max_tokens,
        stop=stop,
        yield_characters=yield_characters,
        tools=tools,
        tool_choice=tool_choice,
        available_functions=available_functions,
    )

    # Create the output folder if it doesn't exist
    logger.debug("audio_output_path: %s", persona_data["audio_output_path"])
    output_dir = create_folder(persona_data["audio_output_path"])

    # Loop until the user says "bye"
    while True:
        # Preparation: Generate the file paths for the audio files.
        human_audio_filepath = get_audio_filepath(
            text="user", file_extension="wav", output_dir=output_dir
        )

        # Step 1: Record audio from the microphone and save it to a file.
        logger.info(
            "Wait in silence to begin recording; wait in silence to terminate...\n"
        )
        detect_audio.record_to_file(human_audio_filepath)
        logger.debug("done - result written to %s\n", human_audio_filepath)

        # Step 2: Convert the audio to text.
        target_language = persona_data["target_language"]
        transcribed_prompt = transcribe_audio.transcribe(
            human_audio_filepath, language=language_codes[target_language]
        )
        logger.info(
            "\033[31mUser: %s\033[0m\n", "\033[33m%s\033[0m" % transcribed_prompt
        )

        # Step 3: Prompt OpenAI's API to generate a response.
        # Save the user input to the persona["messages"] list
        generated_message = generate_message("user", transcribed_prompt)
        persona_data["messages"].append(generated_message)

        # if is_filtered is True, then filter the response
        if is_filtered:
            # Save the filtered response to the persona["messages"] list
            while True:
                try:
                    response = stream_completion.generate_completion(
                        persona=persona_data,  # Contains the conversation data
                        temperature=0.9,
                        stream_mode=True,
                        gpt_model=gpt_model,
                        yield_characters=(".", "?", "!", "\n", ":", ";"),
                        max_tokens=max_tokens,
                        stop=stop,
                        voice=natural_voice,
                        voice_model=voice_model,
                        audio_output_dir=output_dir,
                        tools=tools,
                        tool_choice=tool_choice,
                        available_functions=available_functions,
                    )
                except Exception as error:
                    logger.error("Error: %s", str(error))
                    logger.error(traceback.format_exc())
                    break  # continue
                else:
                    break
        else:
            # Save the unfiltered response to the persona["messages"] list
            response = get_response_unfiltered(human_input=transcribed_prompt)

        # Save the response to the persona["messages"] list
        generated_message = generate_message("assistant", response["last_completion"])
        persona_data["messages"].append(generated_message)
        logger.debug("\nAssistant: %s", generated_message)

        save_conversation(persona_data)
        logger.debug("Saved persona['messages'] = %s", persona_data["messages"])

        # Step 4: Convert the response to audio and play it back to the user.
        # Generate the file path for the audio file, removing spaces from the persona["name"].
        assistant_audio_filepath = response["filepath"]
        logger.debug("assistant_audio_filepath = %s", assistant_audio_filepath)

        # Clean the response from code blocks before synthesizing the audio.
        # response = CodeFilter(text=response).filtered_str # TODO replace, refactor, or remove this line.

        # If natural_voice is None, then use the default voice, else use the natural voice.
        if natural_voice is None:
            logger.info("natural_voice is None, Microsoft voice is used instead.")
            # Get a speech synthesizer
            speech_synthesizer = get_speech_synthesizer(
                selected_voice, assistant_audio_filepath
            )

            # Generate the audio file
            speak_text_into_file(speech_synthesizer, response["last_completion"])
            logger.info(
                "Audio file generated. Content: %s", response["last_completion"]
            )

        # Calculate the duration of the audio file
        duration = get_audio_duration(assistant_audio_filepath)
        logger.debug(
            "Audio file: %s; duration = %s", repr(assistant_audio_filepath), duration
        )

        # Create a VRChat instance
        vrchat = VRChat()

        # Split the response into chunks of 144 characters
        response_chunks = vrchat.split_string(response["last_completion"])
        logger.debug("VRChat response_chunks = %s", response_chunks)

        # Send the response to VRChat
        vrchat.send_text_list(response_chunks, duration)
        logger.info("VRChat response_chunks sent.")
        # play_audio(assistant_audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        goodbye_words = ["bye", "goodbye", "adíos", "adios"]

        if any(word in transcribed_prompt.lower() for word in goodbye_words):
            logger.info("Goodbye words detected. Breaking out of the loop.")
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
        audio_file_path = get_audio_filepath(
            output_dir=output_folder, text="JorgeEscobar_human"
        )

        detect_audio.record_to_file(audio_file_path)
        print(f"done - result written to {audio_file_path}")

        # Step 2: Convert the audio to text.
        target_language = persona["target_language"]
        transcribed_prompt = transcribe_audio.transcribe(
            audio_file_path, language=language_codes[target_language]
        )
        print(f"Transcribed prompt: {transcribed_prompt}")

        # Step 3: Convert the response to audio and play it back to the user.
        # Get a speech synthesizer
        speech_synthesizer = get_speech_synthesizer(selected_voice, audio_file_path)

        # Speak the text
        speak_text_into_file(speech_synthesizer, transcribed_prompt)
        play_audio(audio_file_path)

        # If the transcribed_prompt contains "bye." then break out of the loop
        goodbye_words = ["bye", "goodbye", "adíos"]

        if any(word in transcribed_prompt.lower() for word in goodbye_words):
            break


def main():
    hailey_natural_voice = Voice(
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
        design=None,
        preview_url="https://storage.googleapis.com/eleven-public-prod/U1Rx6ByQzXTKXc5wPxu4fXvSRqO2/voices/chQ8GR2cY20KeFjeSaXI/0ea12727-861b-47b8-8acc-ca22acdc93be.mp3",
        settings=None,
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

    ceci = get_voice_by_id("8otMrswOK7DEs0BuIyzd")

    # Run the conversation
    stream_conversation(
        persona_data=persona,  # Contains the conversation data
        gpt_model=persona["gpt_model"],  # The GPT model to be used
        selected_voice=persona["selected_voice"],  # The default voice is used
        natural_voice=ceci,  # Set to None to use the default voice
        voice_model=persona["elevenlabs_voice_model"],  # The voice model to be used
        is_filtered=True,  # Set to False to enable NSFW content
        output_dir=persona["audio_output_path"],  # The output folder for audio files
        max_tokens=2000,  # The max tokens for the response
        tools=tools,  # The tools to be used
        tool_choice=persona["tool_choice"],  # The tool choice
        available_functions=ai_available_functions,  # The available functions
        yield_characters=(".","?","!","\n",":",";"," ",),  # The yield characters, used to split the response into phrases
    )


if __name__ == "__main__":
    main()
