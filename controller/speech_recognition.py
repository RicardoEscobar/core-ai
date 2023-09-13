# This script is used to convert speech to text using Microsoft Azure Speech to Text API.
import os
import azure.cognitiveservices.speech as speechsdk
import logging
from typing import Union, List, Tuple
import asyncio

from load_openai import load_openai
from create_logger import create_logger

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

async def recognize_from_microphone(language: str = "en-US") -> str:
    """This function is used to recognize speech from the microphone using Microsoft Azure Speech to Text API."""
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language=language

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        module_logger.debug("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        module_logger.error("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        raise Exception("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        module_logger.critical("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            module_logger.error("Error details: {}".format(cancellation_details.error_details))
            module_logger.error("Did you set the speech resource key and region values?")
        raise Exception("Speech Recognition canceled: {}".format(cancellation_details.reason))
    
def listening_loop(language: str = "en-US", stop_str: Union[str, Tuple[str]] = None) -> List[str]:
    """This function executes the recognize_from_microphone function inside a while loop. It stops until the word 'bye' is said."""
    if stop_str is None:
        stop_str = ("bye", "adiós")
    elif isinstance(stop_str, str):
        stop_str = (stop_str,)

    transcription = []
    module_logger.info("Speak into your microphone.")
    while True:
        transcription.append(recognize_from_microphone(language=language))
        module_logger.info(transcription[-1])

        # If the last element of the transcription list contains the stop_str, then break the loop
        if any([stop in transcription[-1].lower() for stop in stop_str]):
            break
    
    return transcription

def test_listening_loop():
    """This function is used to test the listening_loop function."""
    try:
        transcription = listening_loop(language="en-US")
    except Exception as exception:
        module_logger.critical("Exception: {}".format(exception))
    else:
        module_logger.info(transcription)

    
def main():
    """Main function"""
    # Test the async function
    transcription = asyncio.run(recognize_from_microphone(language="es-ES"))
    print(transcription)

if __name__ == "__main__":
    main()
