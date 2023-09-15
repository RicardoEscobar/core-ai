# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))


import os

# This is needed to load the path where the mpv player is located.
os.environ["PATH"] += os.pathsep + "E:\\downloads"

import re
import time
from datetime import datetime
import logging
from typing import Tuple, Union, List
from deprecated import deprecated
from pathlib import Path

import openai
from elevenlabs import generate, stream, save
from elevenlabs.api import Voice, VoiceSettings
import tiktoken

from controller.load_openai import load_openai
from controller.create_logger import create_logger
from controller.speech_synthesis import get_speech_synthesizer, speak_text_into_file
from controller.play_audio import play_audio

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
        prompt: str = "Habla como una vtuber chilena, hablas con muchos modismos chilenos, y eres una Tsundere obsesionada con su chat y das inicio al stream. (un parrafo)",
        gpt_model: str = "gpt-4",
        temperature=0.9,
        stream_mode=True,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
        yield_characters: List[str] = None,
    ):
        """Initialize the StreamCompletion class."""
        self.logger = module_logger

        if voice is None:
            self.vtuber_voice = Voice(
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
        
        if yield_characters is None:
            yield_characters = (".", "?", "!", "\n", ":", ";")

        if stop is None:
            stop = ["\n"]

        self.prompt = prompt
        self.gpt_model = gpt_model
        self.yield_characters = yield_characters
        self.temperature = temperature
        self.stream = stream_mode
        self.max_tokens = max_tokens
        self.stop = stop

    def generate_completion(
        self,
        prompt: str = None,
        gpt_model: str = None,
        voice: Voice = None,
        audio_dir_path: str = "./audio",
    ):
        """Generate a completion from the OpenAI API."""

        if prompt is None:
            prompt = self.prompt

        if gpt_model is None:
            gpt_model = self.gpt_model

        if voice is None:
            voice = self.vtuber_voice

        self.audio_stream = generate(
            text=self.completion_generator(prompt, gpt_model=gpt_model),
            voice=voice,
            model="eleven_multilingual_v1",
            stream=True,
        )

        # Play the audio stream
        audio_stream = stream(self.audio_stream)

        # Create the filename as a Path object
        mp3_file_path = Path(audio_dir_path) / StreamCompletion.get_audio_filepath(prompt)

        # Create the folder if it does not exist
        mp3_file_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger.debug("Saving audio to %s", {mp3_file_path.resolve()})

        # Save the audio stream to a file
        save(audio_stream, str(mp3_file_path.resolve()))

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
            filename = StreamCompletion.get_audio_filepath(prompt, file_extension="mp3")

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
            completion_finished = ''.join(completion)
        
        if completion_finished == '':
            self.logger.error("No completion was generated.")
            raise ValueError("No completion was generated.")
        
        # Speak the text into a file
        speak_text_into_file(speech_synthesizer, completion_finished)
    
        # Play the audio file
        play_audio(filename_str)

    def completion_generator(
        self,
        prompt: str = None,
        temperature=0.9,
        stream_mode=True,
        gpt_model=None,
        yield_characters: Tuple[str] = None,
        max_tokens: int = 150,
        stop: Union[str, List[str]] = None,
    ) -> str:
        """This generator function yields the next completion from the OpenAI API from a stream mode openai completion. Each time a sentence is completed, the generator yields the sentence. To detect the end of a sentence, the generator looks for a period, question mark, or exclamation point at the end of the sentence. If the sentence is not complete, then the generator yields None. If the generator yields None, then the caller should call the generator again to get the next completion. If the generator yields a sentence, then the caller should call the generator again to get the next completion. The generator will yield None when the stream is complete."""

        if prompt is None:
            prompt = self.prompt

        if gpt_model is None:
            gpt_model = self.gpt_model

        if yield_characters is None:
            yield_characters = self.yield_characters

        if stop is None:
            stop = self.stop

        # record the time before the request is sent
        start_time = time.time()

        # send a ChatCompletion request
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature,
            stream=stream_mode,  # again, we set stream=True
            max_tokens=max_tokens,
            stop=stop,
        )

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
        self.logger.debug(
            "Full response received {:.2f} seconds after request".format(chunk_time)
        )
        full_reply_content = "".join([m.get("content", "") for m in collected_deltas])

        # Log the full conversation
        self.logger.debug("Full conversation received: %s", full_reply_content)

    @staticmethod
    def get_audio_filepath(
        text: str, filename_len: int = 100, file_extension: str = "mp3"
    ) -> str:
        """Return a filename for the mp3 file.
        args:
            text (str): The text to use to generate the filename.
            filename_len (int, optional): The maximum length of the filename. Defaults to 100.
        returns:
            str: The filename.
        """
        filename = re.sub(r"[^\w\s-]", "", text[:filename_len]).strip()
        filename = re.sub(r"[-\s]+", "-", filename)
        filename = re.sub(r"[.,:;¿?¡!]", "", filename)
        # Add timestamp to filename
        filename = (
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}.{file_extension}"
        )
        return filename

    @staticmethod
    @deprecated(
        reason="This method is no longer needed and will be removed in a future version."
    )
    def tiktoken_example():
        """TODO eliminate this method after refactor"""
        # Get the encoding object for the "cl100k_base" encoding
        enc = tiktoken.get_encoding("cl100k_base")
        assert enc.decode(enc.encode("hello world")) == "hello world"

        # To get the tokeniser corresponding to a specific model in the OpenAI API:
        enc = tiktoken.encoding_for_model("gpt-4")

        # Encode a string into tokens
        tokens = enc.encode("Hello, world!")

        # Count the number of tokens
        num_tokens = len(tokens)

        module_logger.debug("The string has %s tokens.", {num_tokens})


def main():
    """Run the main function."""
    prompt = "Eres una VTuber Mexicana tipo 'mommy' y consuelas a tu chat. (una oracion)"
    stream_completion = StreamCompletion()
    # stream_completion.generate_completion(
    #     prompt=prompt,
    #     gpt_model="gpt-4",
    # )

    while True:
        try:
            stream_completion.generate_microsoft_ai_speech_completion(
                prompt=prompt,
                gpt_model="gpt-4",
                selected_voice="Yolanda",
            )
        except Exception as exception:
            module_logger.error(exception)
            continue
        else:
            break



if __name__ == "__main__":
    main()
