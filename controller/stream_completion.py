"""This module handles the stream completion from the OpenAI API."""

# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))


import os

# This is needed to load the path where the mpv player is located."C:\Users\Ricardo\Downloads\mpv.exe"
os.environ["PATH"] += os.pathsep + r"C:\Users\Ricardo\Downloads"

import re
import time
from datetime import datetime
import logging
from typing import Tuple, Union, List, Dict
from pathlib import Path
from controller.custom_thread import CustomThread
from pathlib import Path

import openai
from elevenlabs import generate, stream, save, voices
from elevenlabs.api import Voice, VoiceSettings

from controller.load_openai import load_openai
from controller.create_logger import create_logger
from controller.speech_synthesis import get_speech_synthesizer, speak_text_into_file
from controller.play_audio import play_audio
from controller.time_it import time_it
from controller.get_audio_filepath import get_audio_filepath


load_openai()

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
        voice: Voice = None,
        voice_model: str = "eleven_multilingual_v2",
        prompt: str = "Habla como una vtuber chilena, hablas con muchos modismos chilenos, y eres una Tsundere obsesionada con su chat y das inicio al stream. (un parrafo)",
        gpt_model: str = "gpt-4",
        temperature=0.9,
        stream_mode=True,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
        yield_characters: Tuple[str] = None,
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
        self.prompt = prompt
        self.gpt_model = gpt_model
        self.yield_characters = yield_characters
        self.temperature = temperature
        self.stream_mode = stream_mode
        self.max_tokens = max_tokens
        self.stop = stop

        # Saves the last completion generated.
        self.last_completion = ""

    def generate_completion(
        self,
        prompt: str = None,
        temperature=0.9,
        stream_mode=True,
        gpt_model: str = None,
        yield_characters: Tuple[str] = None,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
        voice: Voice = None,
        audio_dir_path: str = "./audio",
        voice_model: str = "eleven_multilingual_v2",
        filename_length: int = 100,
        output_dir: str = ".",
    ) -> Dict[str, str]:
        """Generate a completion from the OpenAI API.
        args:
            prompt (str, optional): The prompt to use. Defaults to None.
            temperature (float, optional): The temperature to use. Defaults to 0.9.
            stream_mode (bool, optional): Whether to use stream mode. Defaults to True.
            gpt_model (str, optional): The GPT model to use. Defaults to None.
            yield_characters (Tuple[str], optional): The characters to yield. Defaults to None.
            max_tokens (int, optional): The maximum number of tokens to use. Defaults to 150.
            stop (Union[str, List[str]], optional): The stop characters to use. Defaults to None.
            voice (Voice, optional): The voice to use. Defaults to None.
            audio_dir_path (str, optional): The directory path to save the audio to. Defaults to "./audio".
            voice_model (str, optional): The voice model to use. Defaults to "eleven_multilingual_v2".

        returns:
            Dict[str, str]: Generated response from the OpenAI API and the filepath of the audio file e. g. {"last_completion": "Hello world!", "filepath": "./audio/20210901_123456_Hello_world.mp3"}
        """

        # Initialize the variables
        if prompt is None:
            prompt = self.prompt

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

        self.logger.debug("Creating a text generator with: '%s'", prompt)
        # Create a text generator
        phrase_generator = self.completion_generator(
            prompt=prompt,
            temperature=temperature,
            stream_mode=stream_mode,
            gpt_model=gpt_model,
            yield_characters=yield_characters,
            max_tokens=max_tokens,
            stop=self.stop,
        )
        self.logger.debug("phrase_generator created: %s", phrase_generator)

        self.audio_stream = generate(
            text=phrase_generator,
            voice=voice,
            model=voice_model,
            stream=stream_mode,
        )
        self.logger.debug("audio_stream created: %s", self.audio_stream)

        # Play the audio stream
        play_audio_stream = stream(self.audio_stream)
        self.logger.debug("play_audio_stream created: %s", play_audio_stream)

        # Create the filename as a Path object
        if self.last_completion == "":
            filename = get_audio_filepath(
                prompt, filename_length, output_dir=output_dir
            )
        else:
            filename = self.last_completion[:filename_length]

        self.logger.debug("filename created: %s", filename)

        mp3_filepath = Path(
            get_audio_filepath(
                filename,
                file_extension="mp3",
                filename_length=filename_length,
                output_dir=output_dir,
            )
        )
        self.logger.debug("mp3_filepath created: %s", mp3_filepath)

        # Create the folder if it does not exist
        mp3_filepath.parent.mkdir(parents=True, exist_ok=True)

        self.logger.debug("Saving audio to %s", {mp3_filepath.resolve()})

        # Save the audio stream to a file
        mp3_file = str(mp3_filepath.resolve())
        save(play_audio_stream, mp3_file)

        return {"last_completion": self.last_completion, "filepath": mp3_file}

    def generate_microsoft_ai_speech_completion(
        self,
        prompt: str = None,
        gpt_model: str = "gpt-4",
        selected_voice: str = "Larissa",
        audio_dir_path: str = "./audio",
        filename: str = None,
        yield_characters: List[str] = None,
        temperature=0.9,
        stream_mode=True,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
    ) -> None:
        """Generate a completion from the Microsoft AI Speech API.
        args:
            prompt (str, optional): The prompt to use. Defaults to None.
            filename (str, optional): The filename to save the audio to. Defaults to None.
        returns:
            str: The generated audio file path.
        """
        if prompt is None:
            prompt = self.prompt

        if filename is None or filename == "":
            filename = get_audio_filepath(prompt, file_extension="mp3")

        if yield_characters is None:
            yield_characters = self.yield_characters

        # Add the directory path to the filename
        filepath = Path(audio_dir_path) / filename
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
        prompt: Union[str, Dict] = None,
        temperature=0.9,
        stream_mode=True,
        gpt_model=None,
        yield_characters: Tuple[str] = None,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
    ):
        """This generator function yields the next completion from the OpenAI API from a stream mode openai completion. Each time a sentence is completed, the generator yields the sentence. To detect the end of a sentence, the generator looks for a period, question mark, or exclamation point at the end of the sentence. If the sentence is not complete, then the generator yields None. If the generator yields None, then the caller should call the generator again to get the next completion. If the generator yields a sentence, then the caller should call the generator again to get the next completion. The generator will yield None when the stream is complete.
        args:
            prompt (str, optional): The prompt to use. Defaults to None.
            temperature (float, optional): The temperature to use. Defaults to 0.9.
            stream_mode (bool, optional): Whether to use stream mode. Defaults to True.
            gpt_model (str, optional): The GPT model to use. Defaults to None.
            yield_characters (Tuple[str], optional): The characters to yield. Defaults to None.
            max_tokens (int, optional): The maximum number of tokens to use. Defaults to 150.
            stop (Union[str, List[str]], optional): The stop characters to use. Defaults to None.
        yields:
            str: The next completion."""

        # Reset the last completion
        self.last_completion = ""

        if prompt is None:
            prompt = self.prompt

        if gpt_model is None:
            gpt_model = self.gpt_model

        if yield_characters is None:
            yield_characters = self.yield_characters

        if stop is None:
            stop = self.stop

        if isinstance(prompt, str):
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        elif isinstance(prompt, dict):
            messages = prompt["messages"]
        else:
            self.logger.error("prompt must be a str or a dict.")
            raise ValueError("prompt must be a str or a dict.")

        # record the time before the request is sent
        start_time = time.time()

        # send a ChatCompletion request
        try:
            response = openai.ChatCompletion.create(
                model=gpt_model,
                messages=messages,
                temperature=temperature,
                stream=stream_mode,  # again, we set stream=True
                max_tokens=max_tokens,
                stop=stop,
            )
        except openai.error.OpenAIError as error:
            self.logger.error("OpenAIError: %s", error)
            raise error
        except Exception as error:
            self.logger.error("From OpenAIError as Exception: %s", error)
            raise error

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
            chunk_delta = chunk["choices"][0]["delta"]  # extract the delta content
            collected_deltas.append(chunk_delta)  # save the delta content
            # if chunk_delta dict contains "role" key or is an emtpy dict, then is not a sentence
            if "role" in chunk_delta or not chunk_delta:
                self.logger.debug(
                    "Message received {:.2f} seconds after request: {}".format(
                        chunk_time, chunk_delta
                    )
                )
                continue
            else:
                # if the chunk is a sentence, then yield the sentence
                if chunk_delta["content"] != "":
                    sentence += chunk_delta["content"]

                # check if the sentence is complete, yield the sentence
                if chunk_delta["content"].endswith(yield_characters):
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

            self.logger.debug(
                "Message received {:.2f} seconds after request: {}".format(
                    chunk_time, chunk_delta
                )
            )

        # Log the time delay and text received
        self.logger.info(
            "Full response received {:.2f} seconds after request".format(chunk_time)
        )
        full_reply_content = "".join([m.get("content", "") for m in collected_deltas])

        # Log the last completion
        self.logger.info("Last completion: %s", full_reply_content)

        # Save last completion
        self.last_completion = full_reply_content


@time_it
def test_generate_completion():
    """Test the generate_completion method."""
    stream_completion = StreamCompletion()
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
        model="eleven_multilingual_v2",
    )
    stream(audio_stream)


@time_it
def main():
    """Run the main function."""
    test_generate_completion()


if __name__ == "__main__":
    main()
