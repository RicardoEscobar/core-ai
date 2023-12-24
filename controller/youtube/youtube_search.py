"""This module is used to control the youtube api."""
import os
import sys

# Add project root to PYTHONPATH
root_folder = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if root_folder not in sys.path:
    sys.path.append(root_folder)

from typing import List
from pathlib import Path
import json
import requests

from pytube import Channel, YouTube, Search
from youtube_transcript_api import YouTubeTranscriptApi

from controller.clean_filename import clean_filename
from controller.load_openai import load_openai


# Load YouTube API key
load_openai()

def get_video_description(video_url: str) -> str:
    """Get the description of a video.
    args:
        video_url: The url of the video.
    returns:
        The description of the video."""
    # Get the video id
    video_id = video_url.split("=")[-1]

    # Get the video description
    api_key = os.getenv("YOUTUBE_API_KEY")
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    response = requests.get(url)
    response_json = response.json()
    video_description = response_json["items"][0]["snippet"]["description"]

    return video_description


def youtube_search(query: str) -> List[YouTube]:
    """Search for a video on YouTube and return the video id.
    args:
        query: The query to search for.
    returns:
        A list of YouTube videos."""
    # Search for the video
    search = Search(query)

    return search.results


def get_transcript(video: YouTube) -> str:
    """Get the transcript of a video.
    args:
        video: The video to get the transcript of.
    returns:
        The transcript of the video."""
    # get the video captions/subtitles as a list of dictionaries
    video_data = YouTubeTranscriptApi.get_transcript(
        video_id=video.video_id, languages=["es-MX", "en-US", "es", "en"]
    )

    # loop through the list of dictionaries and get the transcript
    result = ""
    for data in video_data:
        result += f"{data['text']}"

    return result


def youtube_query(
    query: str, max_videos: int = 1, language: str = "Spanish", max_tokens: int = 500
):
    """Search for a query on YouTube and return the transcript content of the videos. By default, only one video is summarized.
    If the argument max_videos is greater than 1, then that number of videos will be summarized and yielded.
    If language is "Spanish", then the video will be transcripted in Spanish using the Spanish language version of the video.
    max_tokens is the maximum number of tokens for the AI model to use on the transcript text.
    args:
        query: The query to search for.
        max_videos: The maximum number of videos to summarize.
        language: The language of the video transciption.
        max_tokens: The maximum number of tokens for the AI model to use for each video.
    yields:
        A summary of the video."""
    videos = youtube_search(query)
    for video in videos[:max_videos]:
        channel = Channel(video.channel_url)
        result = {
            "query": query,
            "filename": clean_filename("_".join((video.video_id, video.title)))
            + ".json",
            "channel_name": channel.channel_name,
            "channel_url": channel.channel_url,
            "chanel_id": channel.channel_id,
            "video_name": video.title,
            "video_url": video.watch_url,
            "video_id": video.video_id,
            "video_description": get_video_description(video.watch_url),
            "transcript": get_transcript(video),
        }

        yield result


# Import this function to the ai_functions.py file.
def ai_youtube_search(
    prompt: str,
    output_dir: str = "./video_caption",
    max_videos: int = 1,
    max_tokens: int = 500,
) -> str:
    """Search for a video on YouTube and return the transcript.
    args:
        prompt: The prompt to search for on YouTube.
        output_dir: The directory to save the transcript to.
        max_videos: The maximum number of videos to summarize.
        max_tokens: The maximum number of tokens for the AI model to use for each video.
    returns:
        A transcript of the video and metadata of the video."""
    # Make the output directory
    output_dirpath = Path(output_dir) / f"{clean_filename(prompt)}"
    output_dirpath.mkdir(exist_ok=True)

    result = list()
    for data in youtube_query(prompt, max_videos=max_videos, max_tokens=max_tokens):
        output_filepath = output_dirpath / f"{data['filename']}"
        with open(str(output_filepath), "w", encoding="utf-8") as file:
            file.write(json.dumps(data))
            result.append(data)

    return json.dumps(result)


def main():
    """The main function."""
    query = "EVE Online | Down the Rabbit Hole"
    result = json.loads(ai_youtube_search(query))
    print(f"The video transcript is:\n{result[0]['filename']}")


if __name__ == "__main__":
    main()
