# Note: you need to be using OpenAI v1 for the code below to work
from typing import Literal

from controller.load_openai import load_openai


# Load the OpenAI API key from the .env file
client = load_openai()

language_codes = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Belarusian": "be",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese": "zh",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "German": "de",
    "Greek": "el",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Korean": "ko",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Macedonian": "mk",
    "Malay": "ms",
    "Marathi": "mr",
    "Maori": "mi",
    "Nepali": "ne",
    "Norwegian": "no",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog": "tl",
    "Tamil": "ta",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy",
}


def transcribe(
    audio_file: str,
    model: str = "whisper-1",
    language: str = language_codes["Spanish"],
    response_format: str = "text",
) -> str:
    """Transcribe an audio file using the OpenAI API."""
    file = open(audio_file, "rb")
    transcript = client.audio.transcriptions.create(
        file=file,
        model=model,
        language=language,
        response_format=response_format,
    )

    return transcript


def translate(
    audio_file: str,
    model: str = "whisper-1",
    response_format: str = "text",
) -> str:
    file = open(audio_file, "rb")
    translation = client.audio.translations.create(
        file=file,
        model=model,
        response_format=response_format,
    )

    return translation


def main():
    transcribe("prompt.wav")


if __name__ == "__main__":
    main()
