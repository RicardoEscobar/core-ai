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


def get_transcript(video_id):
    """Get the captions/subtitles from a YouTube Video."""

    # get the video captions/subtitles as a list of dictionaries
    video_data = YouTubeTranscriptApi.get_transcript(video_id=video_id)

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


def get_sumarized_text(text: str, ai_model: str = "gpt-4") -> str:
    """
    Given a text, return a summary of the text.
    The text is too long when the token count is greater than half the token limit of the given AI model.
    """

    # Get the token limit for the specified model
    token_limit = TOKEN_LIMITS[ai_model] // 2

    # Get the token count for the text
    token_count = get_token_count(text)

    # If the token count is greater than half the token limit then return True
    if is_prompt_too_big(text, ai_model):
        raise ValueError("The text is too long to be summarized.")
    else:
        # Get the summarized text
        while True:
            retries = 0
            try:
                response = openai.ChatCompletion.create(
                    model=ai_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Summarize content you are provided with for a second-grade student.",
                        },
                        {"role": "user", "content": text},
                    ],
                    temperature=1.0,
                    max_tokens=token_limit,
                    stop=["\n", " Human:", " AI:"],
                )
                sleep(2)  # Wait 2 seconds after each request
            except openai.error.RateLimitError as rate_limit_error:
                print("Rate limit error. Waiting 2 seconds before trying again.")
                sleep(2)
                if retries < 3:
                    retries += 1
                    print(f"Retrying. Attempt {retries} of 3.")
                    continue
                else:
                    print("Maximum retries reached. Aborting.")
                    break
            else:
                break

        result = response.choices[0].message.content
        return result


def main():
    CHARACTER_LIMIT = 1000
    AI_MODEL = "gpt-4"
    # assign the video url to the variable
    video_id = "UMbjeGLF_MY"
    # save_transcript(video_id)
    text = get_transcript(video_id)
    # Get list of segments
    segments = split_text_into_segments(text, CHARACTER_LIMIT)
    print(segments)
    # Get the summarized text from a for loop
    summarized_text = ""
    for index, segment in enumerate(segments):
        print(f"Summarizing segment: {index + 1}/{len(segments)}")
        summarized_segment = get_sumarized_text(segment, AI_MODEL)
        print(summarized_segment)
        summarized_text += summarized_segment + "\n"

    # Save the summarized text to a file
    directory = Path(__file__).parent.parent / "video_caption"
    filename = "summarized_text.txt"
    filepath = directory / filename
    with open(filepath, mode="w", encoding="utf-8") as file:
        file.write(summarized_text)


if __name__ == "__main__":
    main()
