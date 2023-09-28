"""This script is used to convert speech to text using Microsoft Azure Speech to Text API."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import os
import azure.cognitiveservices.speech as speechsdk
import logging
from typing import Union, List, Tuple
import asyncio
import threading
import pyaudio
import numpy as np
from pathlib import Path

from controller.load_openai import load_openai
from controller.create_logger import create_logger
from controller.get_token_count import get_token_count
from controller.custom_thread import CustomThread

# Create logger
module_logger = create_logger(
    logger_name="speech_recognition",
    logger_filename="speech_recognition.log",
    log_directory="logs",
    add_date_to_filename=False,
    console_logging=True,
    console_log_level=logging.INFO,
)

# Load OpenAI API
load_openai()


# Function to check for sound
def listen_mic(
    max_tokens: int = 150,
    stop_str: str = None,
    gpt_model: str = "gpt-4",
    language: str = "es-ES",
) -> str:
    """This function is used to check for sound and then execute the listening_loop function."""

    # Set the stop_str
    if stop_str is None:
        stop_str = ["bye", "adiós"]
    elif isinstance(stop_str, str):
        stop_str = [stop_str]

    # Set the microphone parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 500  # Adjust this threshold to suit your environment

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Listening for sound...")

    result = list()
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        if np.max(data) > THRESHOLD:
            module_logger.info("Sound detected!")
            result = get_transcript(
                language=language,
                stop_str=stop_str,
                max_tokens=max_tokens,
                gpt_model=gpt_model,
            )
            save_transcript(result, filename="transcript.txt")
            module_logger.info("> %s", result)

            # Yield the last element of the result list
            # yield result[-1] # Can't make this work at this time


def recognize_from_microphone(
    language: str = "en-US", speech_key: str = None, speech_region: str = None
) -> str:
    """This function is used to recognize speech from the microphone using Microsoft Azure Speech to Text API."""

    if speech_key is None:
        speech_key = os.environ.get("SPEECH_KEY")
    if speech_region is None:
        speech_region = os.environ.get("SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        module_logger.debug("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        module_logger.error(
            "No speech could be recognized: %s",
            speech_recognition_result.no_match_details,
        )
        raise Exception(
            "No speech could be recognized: {}".format(
                speech_recognition_result.no_match_details
            )
        )
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        module_logger.critical(
            "Speech Recognition canceled: {}".format(cancellation_details.reason)
        )
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            module_logger.error(
                "Error details: {}".format(cancellation_details.error_details)
            )
            module_logger.error(
                "Did you set the speech resource key and region values?"
            )
        raise Exception(
            "Speech Recognition canceled: {}".format(cancellation_details.reason)
        )


def get_transcript(
    language: str = "en-US",
    stop_str: Union[str, Tuple[str]] = None,
    max_tokens: int = 150,
    gpt_model: str = "gpt-4",
) -> List[str]:
    """This function executes the recognize_from_microphone function inside a while loop. It stops until the word 'bye' is said."""
    if stop_str is None:
        stop_str = ("bye", "adiós")
    elif isinstance(stop_str, str):
        stop_str = (stop_str,)

    transcription = []
    module_logger.info("Speak into your microphone.")
    while True:
        try:
            transcription.append(recognize_from_microphone(language=language))
            module_logger.info(transcription[-1])
        except KeyboardInterrupt as exception:
            module_logger.error("Exception: {}".format(exception))
            break
        except Exception as exception:
            module_logger.warning(
                "Exception: {}\Traceback:{}".format(exception, exception.__traceback__)
            )
            continue

        # count tokens and break if max_tokens is reached
        num_tokens = get_token_count(" ".join(transcription), gpt_model=gpt_model)
        module_logger.info("tokens: %s", max_tokens - num_tokens)

        # If the last element of the transcription list contains the stop_str, then break the loop
        if (
            any([stop in transcription[-1].lower() for stop in stop_str])
            or num_tokens >= max_tokens
        ):
            break

    return transcription


def test_listening_loop():
    """This function is used to test the listening_loop function."""
    try:
        transcription = get_transcript(language="es-ES")
        save_transcript(transcription, filename="transcript.txt")
        # transcription = listening_loop(language="en-US")
    except Exception as exception:
        module_logger.critical("Exception: {}".format(exception))
    else:
        module_logger.info(transcription)

def save_transcript(transcription: List[str], filename: str = "transcript.txt"):
    """This function is used to save the transcript to a file."""
    filepath = Path(filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write("\n".join(transcription))

def read_transcript(filename: str = "transcript.txt") -> List[str]:
    """This function is used to read the transcript from a file."""
    filepath = Path(filename)
    with open(filepath, "r", encoding="utf-8") as file:
        return file.readlines()

def main():
    """Main function"""
    # Create a thread to check for sound
    text = ""
    thread = CustomThread(
        target=listen_mic,
        kwargs={
            "max_tokens": 20,
            "stop_str": ["adiós", "bye"],
            "gpt_model": "gpt-4",
            "language": "es-ES",
        },
        daemon=False,
    )
    thread.start()
    # text = thread.join()
    # print(f"text: {text}")


if __name__ == "__main__":
    main()
