# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))


import os

os.environ["PATH"] += os.pathsep + "E:\\downloads"

import re
import wave
import time
from datetime import datetime
import logging
from typing import Tuple

import openai
from elevenlabs import generate, stream, save
from elevenlabs.api import Voice, VoiceSettings
import pyaudio
import tiktoken

from controller.load_openai import load_openai
from controller.create_logger import create_logger
from controller.waifuai.record_voice import save_wav_file

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
        token_threshold: int = 2000,  # 2000 tokens is half the max tokens allowed by GPT-3.5-Turbo model
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

        self.prompt = prompt
        self.gpt_model = gpt_model
        self.token_threshold = token_threshold

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
            text=self.completion_generator(self.prompt, gpt_model=gpt_model),
            voice=self.vtuber_voice,
            model="eleven_multilingual_v1",
            stream=True,
        )

        # Play the audio stream
        audio_stream = stream(self.audio_stream)

        # Create the filename as a Path object
        mp3_file_path = Path(audio_dir_path) / StreamCompletion.get_mp3_filename(
            self.prompt
        )

        # Create the folder if it does not exist
        mp3_file_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Saving audio to {mp3_file_path.resolve()}")

        # Save the audio stream to a file
        save(audio_stream, str(mp3_file_path.resolve()))

    def completion_generator(
        self,
        prompt: str = None,
        temperature=0.9,
        stream=True,
        gpt_model=None,
        yield_characters: Tuple[str] = None,
    ) -> str:
        """This generator function yields the next completion from the OpenAI API from a stream mode openai completion. Each time a sentence is completed, the generator yields the sentence. To detect the end of a sentence, the generator looks for a period, question mark, or exclamation point at the end of the sentence. If the sentence is not complete, then the generator yields None. If the generator yields None, then the caller should call the generator again to get the next completion. If the generator yields a sentence, then the caller should call the generator again to get the next completion. The generator will yield None when the stream is complete."""

        if prompt is None:
            prompt = self.prompt

        if gpt_model is None:
            gpt_model = self.gpt_model

        if yield_characters is None:
            yield_characters = (".", "?", "!", "\n", ":", ";")

        # record the time before the request is sent
        start_time = time.time()

        # send a ChatCompletion request to count to 100
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature,
            stream=stream,  # again, we set stream=True
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
                module_logger.debug(
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
                    print(response, end="", flush=True)
                    if response.endswith((" ", ".", "?", "!")):
                        yield response
                    else:
                        yield response + " "

            module_logger.debug(
                "Message received {:.2f} seconds after request: {}".format(
                    chunk_time, chunk_delta
                )
            )

        # print the time delay and text received
        module_logger.debug(
            "Full response received {:.2f} seconds after request".format(chunk_time)
        )
        full_reply_content = "".join([m.get("content", "") for m in collected_deltas])
        module_logger.debug("Full conversation received: %s", full_reply_content)

    @staticmethod
    def get_mp3_filename(text: str) -> str:
        """Return a filename for the mp3 file."""
        filename = re.sub(r"[^\w\s-]", "", text[:100]).strip()
        filename = re.sub(r"[-\s]+", "-", filename)
        filename = re.sub(r"[.,:;¿?¡!]", "", filename)
        # Add timestamp to filename
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}.mp3"
        return filename
    
    @staticmethod
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

        print(f"The string has {num_tokens} tokens.")



def main():
    """Run the main function."""
    stream_completion = StreamCompletion()
    stream_completion.generate_completion()



if __name__ == "__main__":
    main()
