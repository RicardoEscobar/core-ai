# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
from controller.load_openai import load_openai


# Load the OpenAI API key from the .env file
client = load_openai()

def transcribe(audio_file_path: str) -> str:
    audio_file= open(audio_file_path, "rb")
    transcript = client.audio.transcriptions.create("whisper-1", audio_file)
    
    return transcript['text']

def translate(audio_file_path: str) -> str:
    audio_file= open(audio_file_path, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    return transcript['text']

def main():
    transcribe("prompt.wav")

if __name__ == "__main__":
    main()