import os
import openai
from dotenv import load_dotenv

def load_openai():
    # Load environment variables from .env file
    load_dotenv()

    # Set the OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == '__main__':
    load_openai()