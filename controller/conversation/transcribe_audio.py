# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

audio_file= open("output.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(f"Texto: {transcript['text']}")