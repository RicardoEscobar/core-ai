"""Testing grounds for the new text to speech system. It should sound more natural than the old one."""
if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
from typing import Union
from pathlib import Path
import subprocess
import logging

from elevenlabs import generate, play, voices, save
from elevenlabs.api import Voices, Voice, VoiceSettings

from controller.load_openai import load_openai


# Load environment variables from .env file
load_openai()

def convert_wav(input_file, output_file, skip_existing=False):
    if skip_existing and os.path.exists(output_file):
        print(f"Skipping conversion because output file '{output_file}' already exists.")
        return

    command = ['ffmpeg', '-i', input_file, '-c:a', 'pcm_s16le', output_file]
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        print("Conversion completed successfully.")
    except subprocess.CalledProcessError as error:
        print("Conversion failed with error:", error.output)

def generate_multilingual(
    text: str = "¡Hola! Mi nombre es Arnold, encantado de conocerte!",
    voice: Union[str, Voice] = "Arnold",
    audio_file: str = "multilingual.mp3",
):
    """The eleven_multilingual_v2 model supports multiple languages, including
    English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi."""
    # Set logging level
    logging.basicConfig(level=logging.ERROR)

    # Generate the audio.
    audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")

    # Save the audio to a file.
    audio_file_path = Path(audio_file)
    non_riff_audio = Path(audio_file_path.stem + "_non_riff" + audio_file_path.suffix).resolve()

    logging.info("Saving non RIFF audio to '%s'.", non_riff_audio)
    save(audio, str(non_riff_audio))

    try:
        logging.info("Converting non RIFF audio to WAV format.")
        # Convert the audio file to WAV format or else it won't play on Windows.
        convert_wav(non_riff_audio, audio_file_path, skip_existing=True)
    except Exception as error:
        logging.error(error)
    else:
        # Remove the non-riff audio file.
        non_riff_audio.unlink()


def get_voices():
    """List all your available voices with voices()."""
    voices_list = voices()
    audio = generate(text="Hello there!", voice=voices_list[0])
    print(voices_list)


def get_voice_info(name: str = "Hailey"):
    """Get information about a specific voice with Voices()."""
    voices = Voices.from_api()
    print(voices.__len__())
    print(repr(voices[9]))


def main():
    """Testing grounds for the new text to speech system. It should sound more natural than the old one."""
    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
    lumine_voice = Voice(
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

    # Save the list of voices to a file.
    with open("voices.json", "w", encoding="utf-8") as file:
        file.write(voices().model_dump_json())
    
    # get_voice_info()


if __name__ == "__main__":
    main()
