"""Testing grounds for the new text to speech system. It should sound more natural than the old one."""
import os
from typing import Union
from pathlib import Path

from elevenlabs import generate, play, voices, save
from elevenlabs.api import Voices, Voice, VoiceSettings

from controller.conversation.load_openai import load_openai

# Load environment variables from .env file
load_openai()


def generate_multilingual(
    text: str = "¡Hola! Mi nombre es Arnold, encantado de conocerte!",
    voice: Union[str, Voice] = "Arnold",
    audio_file: str = "multilingual.mp3",
):
    """The eleven_multilingual_v1 model supports multiple languages, including
    English, German, Polish, Spanish, Italian, French, Portuguese, and Hindi."""
    audio = generate(text=text, voice=voice, model="eleven_multilingual_v1")

    # Save the audio to a file.
    audio_file_path = Path(audio_file)
    save(audio, str(audio_file_path.resolve()))


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

    generate_multilingual(text="¡Hola! Mi nombre es Lumina, encantada de conocerte.", voice=lumine_voice)
    # get_voices()
    # get_voice_info()


if __name__ == "__main__":
    main()
