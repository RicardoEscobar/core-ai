# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe(audio_file_path: str) -> str:
    audio_file= open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def main():
    transcribe("prompt.wav")

if __name__ == "__main__":
    main()