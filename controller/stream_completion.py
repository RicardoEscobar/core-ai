"""This module handles the stream completion from the OpenAI API."""

# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))


import time
from datetime import datetime
import logging
from typing import Tuple, Union, List, Dict
from pathlib import Path
from controller.custom_thread import CustomThread
from pathlib import Path
import traceback
import json

import openai
from elevenlabs import generate, stream, save, voices
from elevenlabs.api import Voice, VoiceSettings

from controller.load_openai import load_openai
from controller.create_logger import create_logger
from controller.speech_synthesis import get_speech_synthesizer, speak_text_into_file
from controller.play_audio import play_audio
from controller.time_it import time_it
from controller.get_audio_filepath import get_audio_filepath
from controller.conversation_handler import truncate_conversation_persona
from controller.get_token_count import get_token_count_persona
from controller.waifuai.completion_create import save_conversation, generate_message
from controller.waifuai.conversations.vrchat_runa import persona
from controller.vision.eyes import Eyes

# Load the OpenAI API key, elevenlabs API key
client = load_openai()

# Create a logger instance
module_logger = create_logger(
    logger_name="controller.stream_completion",
    logger_filename="stream_completion.log",
    log_directory="logs/",
    console_logging=True,
    console_log_level=logging.INFO,
)


class StreamCompletion:
    """This class handles the stream completion from the OpenAI API."""

    def __init__(
        self,
        persona: Dict[str, str],
        voice: Union[Voice, str] = None,
        voice_model: str = "eleven_turbo_v2",
        gpt_model: str = "gpt-4",
        temperature=0.9,
        stream_mode=True,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
        yield_characters: Tuple[str] = None,
        tools: List[Dict[str, str]] = None,
        tool_choice: str = "auto",
        available_functions=None,
    ):
        """Initialize the StreamCompletion class."""
        self.logger = module_logger

        if voice is None:
            voice = Voice(
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
                preview_url="https://storage.googleapis.com/eleven-public-prod/U1Rx6ByQzXTKXc5wPxu4fXvSRqO2/voices/chQ8GR2cY20KeFjeSaXI/293c3953-463e-42d3-8a92-ccedad1b9280.mp3",
            )

        if yield_characters is None:
            yield_characters = (".", "?", "!", "\n", ":", ";")

        if stop is None:
            stop = ["\n"]

        self.voice = voice
        self.voice_model = voice_model
        self.persona = persona
        self.gpt_model = gpt_model
        self.yield_characters = yield_characters
        self.temperature = temperature
        self.stream_mode = stream_mode
        self.max_tokens = max_tokens
        self.stop = stop

        if tools is None:
            self.tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "take_picture_and_process",
                        "description": "Use this when asked to see something or someone inside VRChat and talk about it.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "The prompt to use.",
                                },
                            },
                            "required": ["prompt"],
                        },
                    },
                },
            ]

        self.tool_choice = tool_choice
        if available_functions is None:
            self.available_functions = (
                {
                    "take_picture_and_process": Eyes.take_picture_and_process,
                },
            )

        # Saves the last completion generated.
        self.last_completion = ""

    def generate_completion(
        self,
        persona: Dict[str, str] = None,
        role: str = "user",
        temperature=0.9,
        stream_mode=True,
        gpt_model: str = None,
        yield_characters: Tuple[str] = None,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
        voice: Voice = None,
        voice_model: str = "eleven_turbo_v2",
        filename_length: int = 100,
        audio_output_dir: str = ".",
        tools: List[Dict[str, str]] = None,
        tool_choice: str = "auto",
        available_functions: Dict = None,
    ) -> Dict[str, str]:
        """Generate a completion from the OpenAI API.
        args:
            persona (Dict[str, str], optional): The prompt to use. Defaults to None.
            role (str, optional): The role to use. Defaults to "user", Values should be: "assistant", "system", "function" or "user".
            temperature (float, optional): The temperature to use. Defaults to 0.9.
            stream_mode (bool, optional): Whether to use stream mode. Defaults to True.
            gpt_model (str, optional): The GPT model to use. Defaults to None.
            yield_characters (Tuple[str], optional): The characters to yield. Defaults to None.
            max_tokens (int, optional): The maximum number of tokens to use. Defaults to 150.
            stop (Union[str, List[str]], optional): The stop characters to use. Defaults to None.
            voice (Voice, optional): The voice to use. Defaults to None.
            audio_output_dir (str, optional): The directory path to save the audio to. Defaults to "./audio".
            voice_model (str, optional): The voice model to use. Defaults to "eleven_turbo_v2".
            tools (List[Dict[str, str]], optional): A list of tools the model may call.
                Currently, only functions are supported as a tool.
                Use this to provide a list of functions the model may generate JSON inputs for. Defaults to None.
            tool_choice (str, optional): The tool choice to use. Defaults to "auto".
            available_functions (Dict, optional): A dictionary of available functions the model may call.
                Use this to provide a list of functions the model may generate JSON inputs for. Defaults to None.

        returns:
            Dict[str, str]: Generated response from the OpenAI API and the filepath of the audio file e. g. {"last_completion": "Hello world!", "filepath": "./audio/20210901_123456_Hello_world.mp3"}
        """

        # Initialize the variables
        if persona is None:
            persona = self.persona

        if gpt_model is None:
            gpt_model = self.gpt_model

        if yield_characters is None:
            yield_characters = self.yield_characters

        if stop is None:
            stop = self.stop

        if stop is None:
            stop = self.stop

        if voice is None:
            voice = self.voice

        if tools is None:
            tools = self.tools

        # Check if persona is a dict
        if not isinstance(persona, dict):
            self.logger.error("persona must be a dict.")
            raise ValueError("persona must be a dict.")

        # Check if persona has a "messages" key
        if "messages" not in persona:
            self.logger.error("persona must have a 'messages' key.")
            raise ValueError("persona must have a 'messages' key.")

        self.logger.debug("Creating a text generator with: %s", repr(persona))
        # Create a text generator
        phrase_generator = self.completion_generator(
            persona=persona,
            temperature=temperature,
            stream_mode=stream_mode,
            gpt_model=gpt_model,
            yield_characters=yield_characters,
            max_tokens=max_tokens,
            stop=self.stop,
            tools=tools,
            tool_choice=tool_choice,
            available_functions=available_functions,
        )

        self.logger.debug("phrase_generator created: %s", phrase_generator)

        audio_stream = generate(
            text=phrase_generator,
            voice=voice.name,
            model=voice_model,
            stream=stream_mode,
        )

        # Play the audio stream
        self.audio_stream = stream(audio_stream)

        # Get the size of the audio stream
        size_in_bytes = len(self.audio_stream)
        size_in_kilobytes = size_in_bytes / 1024
        size_in_megabytes = size_in_kilobytes / 1024

        self.logger.debug(
            "audio_stream created, size: %s bytes, %.2f KB, %.2f MB",
            format(size_in_bytes, ","),
            size_in_kilobytes,
            size_in_megabytes,
        )

        # Create the filename as a Path object
        if self.last_completion == "":
            filename = get_audio_filepath(
                persona["name"], filename_length, output_dir=audio_output_dir
            )
        else:
            filename = self.last_completion[:filename_length]

        self.logger.debug("filename created: %s", filename)

        mp3_filepath = Path(
            get_audio_filepath(
                filename,
                file_extension="mp3",
                filename_length=filename_length,
                output_dir=audio_output_dir,
            )
        )
        self.logger.debug("mp3_filepath created: %s", mp3_filepath)

        # Create the folder if it does not exist
        mp3_filepath.parent.mkdir(parents=True, exist_ok=True)

        self.logger.debug("Saving audio to %s", {mp3_filepath.resolve()})

        # Save the audio stream to a file
        mp3_file = str(mp3_filepath.resolve())
        save(self.audio_stream, mp3_file)

        return {"last_completion": self.last_completion, "filepath": mp3_file}

    def generate_microsoft_ai_speech_completion(
        self,
        prompt: str = None,
        gpt_model: str = "gpt-4",
        selected_voice: str = "Larissa",
        audio_output_dir: str = "./audio",
        filename: str = None,
        yield_characters: List[str] = None,
        temperature=0.9,
        stream_mode=True,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
        tools: List[Dict[str, str]] = None,
        tool_choice: str = "auto",
        available_functions: Dict = None,
    ) -> None:
        """Generate a completion from the Microsoft AI Speech API.
        args:
            prompt (str, optional): The prompt to use. Defaults to None.
            filename (str, optional): The filename to save the audio to. Defaults to None.
        returns:
            str: The generated audio file path.
        """
        if prompt is None:
            prompt = self.persona

        if filename is None or filename == "":
            filename = get_audio_filepath(prompt, file_extension="mp3")

        if yield_characters is None:
            yield_characters = self.yield_characters

        # Add the directory path to the filename
        filepath = Path(audio_output_dir) / filename
        filename_str = str(filepath.resolve())

        # Get the speech synthesizer
        speech_synthesizer = get_speech_synthesizer(
            filename=filename_str, selected_voice=selected_voice
        )

        # Create a variable to hold the completion
        completion_finished = ""

        # Query OpenAI for a completion
        for completion in self.completion_generator(
            prompt,
            temperature=temperature,
            stream_mode=stream_mode,
            gpt_model=gpt_model,
            yield_characters=yield_characters,
            max_tokens=max_tokens,
            stop=stop,
            tools=tools,
            tool_choice=tool_choice,
            available_functions=available_functions,
        ):
            # Wait for the next chunk
            completion_finished = "".join(completion)

        if completion_finished == "":
            self.logger.error("No completion was generated.")
            raise ValueError("No completion was generated.")

        # Speak the text into a file
        speak_text_into_file(speech_synthesizer, completion_finished)

        # Play the audio file
        play_audio(filename_str)

    def completion_generator(
        self,
        persona: Dict[str, str],
        role: str = "user",
        temperature=0.9,
        stream_mode=True,
        gpt_model=None,
        yield_characters: Tuple[str] = None,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
        tools: List[Dict[str, str]] = None,
        tool_choice: str = "auto",
        available_functions: Dict = None,
    ):
        """This generator function yields the next completion from the OpenAI API from a stream mode openai completion. Each time a sentence is completed, the generator yields the sentence. To detect the end of a sentence, the generator looks for a period, question mark, or exclamation point at the end of the sentence. If the sentence is not complete, then the generator yields None. If the generator yields None, then the caller should call the generator again to get the next completion. If the generator yields a sentence, then the caller should call the generator again to get the next completion. The generator will yield None when the stream is complete.
        args:
            persona (Dict[str, str], optional): The prompt to use. Defaults to None.
            role (str, optional): The role to use. Defaults to "user", Values should be: "assistant", "system", "function" or "user".
            temperature (float, optional): The temperature to use. Defaults to 0.9.
            stream_mode (bool, optional): Whether to use stream mode. Defaults to True.
            gpt_model (str, optional): The GPT model to use. Defaults to None.
            yield_characters (Tuple[str], optional): The characters to yield. Defaults to None.
            max_tokens (int, optional): The maximum number of tokens to use. Defaults to 150.
            stop (Union[str, List[str]], optional): The stop characters to use. Defaults to None.
            tools (List[Dict[str, str]], optional): A list of tools the model may call.
                Currently, only functions are supported as a tool.
                Use this to provide a list of functions the model may generate JSON inputs for. Defaults to None.
            tool_choice (str, optional): The tool choice to use. Defaults to "auto".
            available_functions (Dict, optional): A dictionary of available functions the model may call.

        yields:
            str: The next completion."""

        # gpt-4-vision-preview has a max token length of 128,000. Returns a maximum
        # of 4,096 output tokens.So 128_000 - 4096 = 123_904 as the token threshold.
        TOKEN_THRESHOLD = 123_904

        # Reset the last completion
        self.last_completion = ""

        if persona is None:
            raise ValueError("persona must be a dict.")

        if gpt_model is None:
            gpt_model = self.gpt_model

        if yield_characters is None:
            yield_characters = self.yield_characters

        if stop is None:
            stop = self.stop

        if tools is None:
            tools = self.tools

        if tool_choice is None:
            tool_choice = self.tool_choice

        if available_functions is None:
            available_functions = self.available_functions

        # Check if persona is a dict
        if not isinstance(persona, dict):
            self.logger.error("persona must be a dict.")
            raise ValueError("persona must be a dict.")

        # Check if persona has a "messages" key
        if "messages" not in persona:
            self.logger.error("persona must have a 'messages' key.")
            raise ValueError("persona must have a 'messages' key.")

        # Check if persona["messages"] is a list
        if not isinstance(persona["messages"], list):
            self.logger.error("persona['messages'] must be a list.")
            raise ValueError("persona['messages'] must be a list.")

        # Check if persona["messages"] is too long and if so, truncate it
        token_count = get_token_count_persona(persona, gpt_model)
        while token_count > TOKEN_THRESHOLD - max_tokens:
            module_logger.info(
                "persona['messages'] token count = %s is too long for %s limit. Truncating it.",
                token_count,
                gpt_model,
            )

            persona = truncate_conversation_persona(persona)
            self.persona = persona

            # Save the truncated persona to a file
            save_conversation(persona)

            token_count = get_token_count_persona(persona, gpt_model)

        # record the time before the request is sent
        start_time = time.time()

        # In Python, when you assign a list to a variable, the variable holds a
        # reference to the list, not a copy of the list. This means that if you
        # modify the list through the variable, the original list is also
        # modified.
        messages = persona["messages"].copy()

        # Step 1: send the messages and tools to the model
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,  # auto is default, but we'll be explicit
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            if available_functions is None:
                available_functions = self.available_functions
            messages.append(
                response_message
            )  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                function_response = function_to_call(
                    prompt=function_args.get("prompt"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages,
            )  # get a new response from the model where it can see the function response

            # Log the last completion
            full_reply_content = second_response.choices[0].message.content
            self.logger.info(
                "\033[92mAssistant:\033[0m \033[33m%s\033[0m\n", full_reply_content
            )

            # Save last completion
            self.last_completion = full_reply_content

            # required to add a space after the function yield or else audio will throw an error
            yield self.last_completion + " "
        else:
            # TODO THIS IS THE OLD CODE THAT WORKS, BUT DOES NOT SUPPORT FUNTION CALLS
            while True:
                # send a ChatCompletion request
                try:
                    response = client.chat.completions.create(
                        model=gpt_model,
                        messages=persona["messages"],
                        temperature=temperature,
                        stream=stream_mode,  # again, we set stream=True
                        max_tokens=max_tokens,
                        stop=stop,
                    )
                except openai.APITimeoutError as error:
                    # Handle timeout error, e.g. retry or log
                    module_logger.critical(
                        f"openai.APITimeoutError:\nOpenAI API request timed out: {error}\nFull traceback:\n{traceback.format_exc()}"
                    )
                    yield error
                    return  # Stop the function after yielding the error
                except openai.APIConnectionError as error:
                    # Handle connection error, e.g. check network or log
                    module_logger.critical(
                        f"openai.APIConnectionError:\nOpenAI API request failed to connect: {error}\nFull traceback:\n{traceback.format_exc()}"
                    )
                    yield error
                    return  # Stop the function after yielding the error
                except openai.APIResponseValidationError as error:
                    module_logger.critical(
                        f"openai.APIResponseValidationError:\n{error}\nFull traceback:\n{traceback.format_exc()}"
                    )
                    yield error
                    return  # Continue the function after yielding the error
                except openai.APIStatusError as error:
                    # Handle authentication error, e.g. check credentials or log
                    module_logger.critical(
                        f"openai.APIStatusError:\nOpenAI API request was not authorized: {error}\nFull traceback:\n{traceback.format_exc()}"
                    )
                    yield error
                    return  # Stop the function after yielding the error
                except openai.APIError as error:
                    # Handle permission error, e.g. check scope or log
                    module_logger.critical(
                        f"openai.APIError: {error}\nFull traceback:\n{traceback.format_exc()}"
                    )
                    yield error
                    return  # Stop the function after yielding the error
                else:
                    # No error, break the loop
                    break

            # create variables to collect the stream of chunks
            collected_chunks = []
            collected_deltas = []
            sentence = ""

            # iterate through the stream of events
            for chunk in response:
                chunk_time = (
                    time.time() - start_time
                )  # calculate the time delay of the chunk
                collected_chunks.append(chunk)  # save the event response

                chunk_delta = chunk.choices[0].delta
                collected_deltas.append(chunk_delta)  # save the delta content
                # if chunk_delta has no content, then skip it
                if chunk_delta.content == "":
                    self.logger.debug(
                        "Message skipped {:.2f} seconds after request: {}\nRole: {}, content: {}".format(
                            chunk_time,
                            chunk_delta,
                            chunk_delta.role,
                            chunk_delta.content,
                        )
                    )
                    continue
                elif chunk_delta.content:
                    # if the chunk.content is None, then skip it
                    sentence += chunk_delta.content

                    # check if the sentence is complete, yield the sentence
                    if chunk_delta.content.endswith(yield_characters):
                        response = sentence
                        sentence = ""

                        if isinstance(response, str) and response.endswith(
                            (" ", ".", "?", "!")
                        ):
                            # print(response, end="", flush=True)
                            yield response
                        elif isinstance(response, str):
                            # print(response, end="", flush=True)
                            yield response + " "
                        else:
                            raise ValueError(
                                "response must be a string, not {}".format(
                                    type(response)
                                )
                            )

                self.logger.debug(
                    "Message received {:.2f} seconds after request: {}\nRole: {}, content: {}".format(
                        chunk_time, chunk_delta, chunk_delta.role, chunk_delta.content
                    )
                )

            # Log the time delay and text received
            self.logger.info(
                "Full response received {:.2f} seconds after request".format(chunk_time)
            )
            # full_reply_content = "".join([message.content for message in collected_deltas])
            full_reply_content = "".join(
                [
                    message.content if message.content is not None else ""
                    for message in collected_deltas
                ]
            )

            # Log the last completion
            self.logger.info(
                "\033[92mAssistant:\033[0m \033[33m%s\033[0m\n", full_reply_content
            )

            # Save last completion
            self.last_completion = full_reply_content


@time_it
def test_generate_completion():
    """Test the generate_completion method."""
    stream_completion = StreamCompletion(persona=persona)
    stream_completion.generate_completion()


@time_it
def test_get_voices():
    """Test the get_voices method."""

    # Create specific voice
    voice = Voice(
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
        preview_url="https://storage.googleapis.com/eleven-public-prod/U1Rx6ByQzXTKXc5wPxu4fXvSRqO2/voices/chQ8GR2cY20KeFjeSaXI/293c3953-463e-42d3-8a92-ccedad1b9280.mp3",
    )

    print(repr(voice))
    print(type(voice))
    audio_stream = generate(
        text="No se porque se tarda tanto en generar el audio, tal vez es porque el servicio esta saturado.",
        stream=True,
        voice=voice,
        model="eleven_turbo_v2",
    )
    stream(audio_stream)


@time_it
def main():
    """Run the main function."""
    test_generate_completion()


if __name__ == "__main__":
    main()
