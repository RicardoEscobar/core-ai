"""
This module is used for getting the captions/subtitles from a YouTube Video.
pip install youtube-transcript-api # for windows
pip3 install youtube-transcript-api # for linux
"""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))

from typing import List, Dict
from pathlib import Path
from time import sleep

from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import openai

from controller.get_token_count import get_token_count
from controller.load_openai import load_openai
from controller.speech_synthesis import get_speech_synthesizer, speak_text_into_file
from controller.play_audio import play_audio
from controller.get_audio_filepath import get_audio_filepath


# Load the OpenAI API key
load_openai()

# Constants
TOKEN_LIMITS = {
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0613": 32768,
    "gpt-4-0314": 8192,  # Legacy
    "gpt-4-32k-0314": 32768,  # Legacy
    "gpt-3.5-turbo": 4097,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-instruct": 4097,
    "gpt-3.5-turbo-0613": 4097,
    "gpt-3.5-turbo-16k-0613": 16385,
    "gpt-3.5-turbo-0301": 4097,  # Legacy
    "text-davinci-003": 4097,  # Legacy
    "text-davinci-002": 4097,  # Legacy
    "code-davinci-002": 8001,  # Legacy
}

RATE_LIMITS = {
    # Chat rate limits.
    # TPM: Tokens per minute. RPM: Requests per minute.
    # https://platform.openai.com/account/rate-limits
    "gpt-3.5-turbo": {"TPM": 90_000, "RPM": 3_500},
    "gpt-3.5-turbo-0301": {"TPM": 90_000, "RPM": 3_500},
    "gpt-3.5-turbo-0613": {"TPM": 90_000, "RPM": 3_500},
    "gpt-3.5-turbo-16k": {"TPM": 180_000, "RPM": 3_500},
    "gpt-3.5-turbo-16k-0613": {"TPM": 180_000, "RPM": 3_500},
    "gpt-3.5-turbo-instruct": {"TPM": 250_000, "RPM": 3_000},
    "gpt-3.5-turbo-instruct-0914": {"TPM": 250_000, "RPM": 3_000},
    "gpt-4": {"TPM": 10_000, "RPM": 200},
    "gpt-4-0314": {"TPM": 10_000, "RPM": 200},
    "gpt-4-0613": {"TPM": 10_000, "RPM": 200},
}


def get_transcript(video_id):
    """Get the captions/subtitles from a YouTube Video."""

    # get the video captions/subtitles as a list of dictionaries
    video_data = YouTubeTranscriptApi.get_transcript(
        video_id=video_id, languages=["es", "en"]
    )

    # loop through the list of dictionaries and get the text
    result = ""
    for data in video_data:
        result += f"{data['text']} "
    return result


def save_transcript(video_id: str, filename: str = None) -> None:
    # get the captions/subtitles from the video
    text = get_transcript(video_id)
    # get the video title from YouTube
    yt = YouTube("https://youtu.be/" + video_id)
    if filename is None:
        # Create a directory to save the conversation if not exists.
        directory = Path(__file__).parent.parent / "video_caption"
        directory.mkdir(parents=True, exist_ok=True)
        # Saves the conversation to a file.
        directory = Path(__file__).parent.parent / "video_caption"
        filename = yt.title + ".txt"
        # Remove invalid characters from the filename.
        for character in r'[]/\;,><&*:%=+@!#^()|?^"':
            filename = filename.replace(character, "_")
        filepath = directory / filename
    elif isinstance(filename, str):
        # Create a directory to save the conversation if not exists.
        filepath = Path(filename)
    else:
        raise TypeError("filename argument must be a string or None")
    with open(filepath, mode="w", encoding="utf-8") as file:
        file.write(text)


def is_prompt_too_big(text: str, ai_model: str = "gpt-4") -> bool:
    """
    Given a text, ask if the text should be divided into smaller prompts.
    The text is too long when the token count is greater than half the token limit of the given AI model.
    """

    # Get the token limit for the specified model
    token_limit = TOKEN_LIMITS[ai_model]

    # Get the token count for the text
    token_count = get_token_count(text)

    # If the token count is greater than half the token limit then return True
    if token_count > token_limit // 2:
        return True
    else:
        return False


def split_text_into_segments(text, character_limit) -> List[str]:
    # Initialize a list to store the segmented text
    segments = []

    # Split the text into segments of token_limit size or less
    start_index = 0
    while start_index < len(text):
        end_index = start_index + character_limit
        # Ensure we don't split in the middle of a word
        while end_index < len(text) and not text[end_index].isspace():
            end_index -= 1
        segments.append(text[start_index:end_index].strip())
        start_index = end_index + 1  # Move the start_index to the next segment

    return segments


def get_sumarized_text(
    text: str, ai_model: str = "gpt-4", max_tokens: int = 100, language: str = "English"
) -> str:
    """
    Given a text, return a summary of the text.
    The text is too long when the token count is greater than half the token limit of the given AI model.
    """
    # Get the system prompt to be used for the given AI model and ask for a summary of the text
    system_content = f"Summarize content you are provided from a video transcript, for an adult of 100 I.Q. in {language}"
    system_content_token_count = get_token_count(system_content)

    BIGGEST_MODEL = "gpt-3.5-turbo-16k"
    SLEEP_TIME = 60  # seconds

    # Get the token count for the text
    token_count = get_token_count(text)
    used_tokens = system_content_token_count + token_count

    # Get the token limit for the specified model
    token_limit = TOKEN_LIMITS[ai_model] - system_content_token_count

    # If chosen model is too small, then change model to a bigger one.
    if (
        is_prompt_too_big(text, ai_model)
        and token_count < TOKEN_LIMITS[BIGGEST_MODEL] - system_content_token_count
        and ai_model != BIGGEST_MODEL
    ):
        # Change model to "gpt-3.5-turbo-16k": 16385
        token_limit = TOKEN_LIMITS[BIGGEST_MODEL] - used_tokens
        ai_model = BIGGEST_MODEL

    if token_count > token_limit:
        print(f"The text is too long to be summarized: {token_count}/{token_limit}")
        print(f"Difference: {token_count - token_limit}")
        raise ValueError("The text is too long to be summarized.")

    # Get the summarized text
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=ai_model,
                messages=[
                    {
                        "role": "system",
                        "content": system_content,
                    },
                    {"role": "user", "content": text},
                ],
                temperature=1.0,
                max_tokens=max_tokens,
                # stop=["\n", " Human:", " AI:"],
            )
        except openai.error.RateLimitError as rate_limit_error:
            print(
                f"{rate_limit_error}. Waiting {SLEEP_TIME} seconds before trying again."
            )
            sleep(SLEEP_TIME)
            print("Trying again...")
            continue
        else:
            break

    result = response.choices[0].message.content
    return result


def get_yt_video_title(video_id: str) -> str:
    """Get the title of a YouTube video."""
    # Get the title of the YouTube video
    yt = YouTube("https://youtu.be/" + video_id)
    title = yt.title
    # Remove invalid characters from the filename.
    for character in r'[]/\;,><&*:%=+@!#^()|?^"':
        title = title.replace(character, "_")
    return title


def get_yt_summary(
    video_id: str,
    max_tokens: int = 100,
    output_dir: str = None,
    language: str = "English",
) -> str:
    """Given a video id, return the summarized content of the video."""
    AI_MODEL = "gpt-4"

    # Get the output directory as a Path object
    if output_dir is None:
        output_dir_path = Path(__file__).parent.parent / "video_caption"
    elif isinstance(output_dir, str):
        output_dir_path = Path(output_dir)
        if output_dir_path.is_file():
            raise FileExistsError("output_dir argument must be a directory")
        if not output_dir_path.exists():
            output_dir_path.mkdir(parents=True, exist_ok=True)
    else:
        raise TypeError("output_dir argument must be a string or None")

    # save_transcript(video_id)
    video_transcript = get_transcript(video_id)

    # Get the summarized text
    summarized_text = get_sumarized_text(
        video_transcript, AI_MODEL, max_tokens, language
    )

    # Get the title of the YouTube video
    title = get_yt_video_title(video_id)

    # Save the summarized text to a file
    filename = f"summarized_{video_id}_{title}.txt"
    filepath = output_dir_path / filename
    with open(filepath, mode="w", encoding="utf-8") as file:
        file.write(summarized_text)
    
    return summarized_text


def main():
    VIDEO_ID = "beEqgUZKZfw"
    summary = get_yt_summary(
        video_id=VIDEO_ID, max_tokens=200, output_dir=None, language="Spanish"
    )

    DIRECTORY = Path(__file__).parent.parent / "video_caption"

    # Constants for speech synthesis configuration
    SELECTED_VOICE = 'Larissa'
    video_title = get_yt_video_title(VIDEO_ID)

    # Save the summarized text to a file
    filename = f"summarized_{VIDEO_ID}_{video_title}"
    # output_path = Path(__file__).parent.parent / "video_caption"
    # filepath = output_path / filename

    # Generate the file path for the audio file, removing spaces from the persona["name"].
    audio_file = get_audio_filepath(output_dir=DIRECTORY, text=filename)

    # Get a speech synthesizer
    speech_synthesizer = get_speech_synthesizer(SELECTED_VOICE, audio_file)

    # Speak the text
    speak_text_into_file(speech_synthesizer, summary)

    # Play audio file
    play_audio(audio_file)


if __name__ == "__main__":
    main()