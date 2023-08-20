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

from controller.conversation.load_openai import load_openai
from controller.create_logger import create_logger
from controller.conversation.record_voice import save_wav_file

load_openai()

# Create a logger instance
module_logger = create_logger(
    logger_name="controller.stream_completion",
    logger_filename="stream_completion.log",
    log_directory="logs/",
    console_logging=True,
    console_log_level=logging.INFO,
)

def completion_generator(
    prompt,
    max_tokens=100,
    temperature=0.9,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"],
    stream=True,
    model="gpt-3.5-turbo",
    yield_characters: Tuple[str] = None,
) -> str:
    """This generator function yields the next completion from the OpenAI API from a stream mode openai completion. Each time a sentence is completed, the generator yields the sentence. To detect the end of a sentence, the generator looks for a period, question mark, or exclamation point at the end of the sentence. If the sentence is not complete, then the generator yields None. If the generator yields None, then the caller should call the generator again to get the next completion. If the generator yields a sentence, then the caller should call the generator again to get the next completion. The generator will yield None when the stream is complete."""

    if yield_characters is None:
        yield_characters = (":", ";", ",", ".", "¿", "?", "¡", "!")

    # record the time before the request is sent
    start_time = time.time()

    # send a ChatCompletion request to count to 100
    response = openai.ChatCompletion.create(
        model=model,
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
        chunk_time = time.time() - start_time  # calculate the time delay of the chunk
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
                yield response

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

def get_mp3_filename(text: str) -> str:
    """Return a filename for the mp3 file."""
    filename = re.sub(r"[^\w\s-]", "", text[:100]).strip()
    filename = re.sub(r"[-\s]+", "-", filename)
    filename = re.sub(r"[.,:;¿?¡!]", "", filename)
    # Add timestamp to filename
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
    return filename

def main():
    """Run the main function."""

    vtuber_voice = Voice(
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

    prompt = "Habla como una vtuber, Yandere obsesionada con su chat despotricando sobre otras vtubers que puedan robar su atencion. (dos parrafos)"

    audio_stream = generate(
        text=completion_generator(prompt),
        voice=vtuber_voice,
        model="eleven_multilingual_v1",
        stream=True,
    )

    audio_stream = stream(audio_stream)

    save(audio_stream, f"{get_mp3_filename(prompt)}.mp3")


if __name__ == "__main__":
    main()
